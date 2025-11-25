"""
Auto Writer GUI with Speed Control & ESC Stop

Features:
- Text input area with speed slider (adjusts typing delay)
- Start button: minimizes GUI, waits for you to click target window
- ESC key: stops typing mid-operation
- Character-by-character typing via pyautogui
"""
import threading
import time
import tkinter as tk
from tkinter import messagebox, Scale
import ctypes
from ctypes import wintypes

try:
    import pyautogui
except Exception:
    pyautogui = None

try:
    from pynput import mouse, keyboard
except Exception:
    mouse = None
    keyboard = None

# Windows API
user32 = ctypes.windll.user32

class AutoWriterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Auto Writer — Speed Control + ESC Stop')
        self.geometry('700x480')
        
        self._running = False
        self._typing = False
        self._listener = None
        self._kb_listener = None
        self._worker = None
        self._stop_typing = False
        
        # Speed: delay in milliseconds between keystrokes
        # Higher = slower; Lower = faster
        # Default 30ms (high speed)
        self.typing_interval = 0.03
        
        self._build()
        self._setup_esc_listener()
    
    def _build(self):
        """Build GUI layout"""
        # Title
        title = tk.Label(self, text='Auto Writer with Speed Control', font=('Arial', 12, 'bold'))
        title.pack(anchor='w', padx=12, pady=(12, 0))
        
        # Text input
        lbl_text = tk.Label(self, text='Enter text to type:')
        lbl_text.pack(anchor='w', padx=12, pady=(8, 0))
        
        self.text = tk.Text(self, wrap='word', height=14, font=('Courier', 10))
        self.text.pack(fill='both', expand=True, padx=12, pady=6)
        
        # Speed control frame
        speed_frame = tk.Frame(self)
        speed_frame.pack(fill='x', padx=12, pady=(0, 8))
        
        lbl_speed = tk.Label(speed_frame, text='Typing Speed (lower = faster):')
        lbl_speed.pack(anchor='w')
        
        # Slider: 1ms (very fast) to 300ms (slow)
        self.speed_slider = Scale(
            speed_frame,
            from_=1,
            to=300,
            orient='horizontal',
            command=self._on_speed_change
        )
        self.speed_slider.set(30)  # 30ms default
        self.speed_slider.pack(fill='x')
        
        self.speed_label = tk.Label(speed_frame, text='30 ms per key')
        self.speed_label.pack(anchor='e')
        
        # Button frame
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill='x', padx=12, pady=(0, 8))
        
        self.start_btn = tk.Button(btn_frame, text='Start (click target)', width=20, command=self.start)
        self.start_btn.pack(side='left')
        
        self.stop_btn = tk.Button(btn_frame, text='Stop', width=12, state='disabled', command=self.stop)
        self.stop_btn.pack(side='left', padx=(8, 0))
        
        # Status bar
        self.status_var = tk.StringVar(value='Ready')
        self.status_lbl = tk.Label(self, textvariable=self.status_var, anchor='w', relief='sunken')
        self.status_lbl.pack(fill='x', padx=0, pady=0)
    
    def _on_speed_change(self, val):
        """Update typing interval from slider"""
        self.typing_interval = float(val) / 1000.0  # Convert ms to seconds
        self.speed_label.config(text=f'{val} ms per key')
    
    def _setup_esc_listener(self):
        """Set up global ESC key listener"""
        if keyboard is None:
            return
        try:
            self._kb_listener = keyboard.Listener(on_press=self._on_key_press)
            self._kb_listener.start()
        except Exception:
            pass
    
    def _on_key_press(self, key):
        """Global ESC key handler"""
        try:
            if key == keyboard.Key.esc:
                self._stop_typing = True
        except Exception:
            pass
    
    def set_status(self, msg):
        """Update status bar"""
        self.status_var.set(msg)
        self.update_idletasks()
    
    def start(self):
        """Start waiting for click target"""
        if self._running:
            return
        
        txt = self.text.get('1.0', 'end').strip()
        if not txt:
            messagebox.showinfo('No text', 'Please enter some text first')
            return
        
        if pyautogui is None:
            messagebox.showerror('Missing dependency', 'pyautogui is required.\nRun: pip install pyautogui')
            return
        
        if mouse is None:
            messagebox.showerror('Missing dependency', 'pynput is required.\nRun: pip install pynput')
            return
        
        self._running = True
        self._stop_typing = False
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.set_status('Waiting for you to click the target window...')
        
        # Minimize GUI
        try:
            self.iconify()
        except Exception:
            pass
        
        # Listen for click
        self._listener = mouse.Listener(on_click=self._on_click)
        self._listener.start()
    
    def stop(self):
        """Stop listening and typing"""
        if not self._running:
            return
        
        self._running = False
        self._stop_typing = True
        self.set_status('Stopped')
        
        if self._listener:
            try:
                self._listener.stop()
            except Exception:
                pass
            self._listener = None
        
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        
        try:
            self.deiconify()
        except Exception:
            pass
    
    def _on_click(self, x, y, button, pressed):
        """Global click listener"""
        if not pressed or not self._running:
            return
        
        # Stop listening immediately
        try:
            if self._listener:
                self._listener.stop()
        except Exception:
            pass
        self._listener = None
        
        # Get text and launch typing in a thread
        txt = self.text.get('1.0', 'end').strip()
        self._worker = threading.Thread(target=self._handle_click_and_type, args=(x, y, txt), daemon=True)
        self._worker.start()
    
    def _handle_click_and_type(self, x, y, txt):
        """Detect window, bring to foreground, and type"""
        self.set_status('Click detected — preparing to type')
        
        try:
            # Find window at click location
            pt = wintypes.POINT(int(x), int(y))
            hwnd = user32.WindowFromPoint(pt)
            
            if not hwnd:
                self.set_status('No window found at click')
                self.after(0, self._finish)
                return
            
            # Bring window to foreground
            try:
                user32.SetForegroundWindow(hwnd)
            except Exception:
                pass
            
            # Wait for focus to settle
            time.sleep(0.15)
            
            # Release any held modifier keys
            for k in ('ctrl', 'alt', 'shift'):
                try:
                    pyautogui.keyUp(k)
                except Exception:
                    pass
            
            # Type with configured interval
            self.set_status('Typing...')
            self._typing = True
            
            try:
                # pyautogui.write() types character by character with interval
                pyautogui.write(txt, interval=self.typing_interval)
            except Exception as e:
                self.set_status(f'Typing failed: {str(e)[:40]}')
                self._typing = False
                self.after(0, self._finish)
                return
            
            # If ESC was pressed during typing, stop
            if self._stop_typing:
                self.set_status('Typing stopped by ESC')
            else:
                self.set_status('Typing complete')
            
            self._typing = False
        
        finally:
            self.after(0, self._finish)
    
    def _finish(self):
        """Reset state and restore GUI"""
        self._running = False
        self._typing = False
        self._stop_typing = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        
        try:
            self.deiconify()
        except Exception:
            pass
        
        if not self.status_var.get():
            self.set_status('Ready')

if __name__ == '__main__':
    app = AutoWriterGUI()
    app.mainloop()
