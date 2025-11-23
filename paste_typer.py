"""
Auto Paste Typer Tool
Monitors clipboard and automatically types the content when you click in another application.
Press Ctrl+C to copy text, then click anywhere in another application to auto-type it.
Press ESC to exit the program.
"""

import pyperclip
import pyautogui
import keyboard
import time
from threading import Thread
import sys

# Configuration
CLIPBOARD_CHECK_INTERVAL = 0.1  # Check clipboard every 100ms
TYPING_DELAY = 0.01  # Delay between each character when typing
# Safety options
REQUIRE_HOTKEY = False           # If True, require `HOTKEY` to be pressed to type (safer than click)
HOTKEY = 'ctrl+alt+v'            # Hotkey to trigger typing when REQUIRE_HOTKEY is True
CONFIRM_BEFORE_TYPING = False    # (Console-based) ask for Y/N before typing (not reliable if console loses focus)
PREVIEW_CHARS = 120              # Number of chars to show in the preview
IGNORE_STACKTRACE = True         # If True, ignore clipboard contents that look like a Python stack trace

class PasteTyper:
    def __init__(self):
        self.last_clipboard = ""
        self.is_running = True
        self.waiting_for_click = False
        self.clipboard_text = ""
        
    def monitor_clipboard(self):
        """Monitor clipboard for changes"""
        print("📋 Clipboard monitor started. Copy text (Ctrl+C) to start...")
        while self.is_running:
            try:
                current_clipboard = pyperclip.paste()
                
                # Check if clipboard has changed and is not empty
                if current_clipboard != self.last_clipboard and current_clipboard.strip():
                    self.last_clipboard = current_clipboard
                    self.clipboard_text = current_clipboard

                    # Simple heuristic to detect Python tracebacks / stack traces
                    is_stack = False
                    if IGNORE_STACKTRACE:
                        txt = current_clipboard.lstrip()
                        if txt.startswith('Traceback (most recent call last):') or 'Traceback (most recent call last)' in txt:
                            is_stack = True
                        # also detect typical long trace-like content
                        if '\n  File ' in txt and '\nTraceback' in txt:
                            is_stack = True

                    if is_stack:
                        print("\n⚠️  Clipboard looks like a stack trace — ignoring (enable/disable with IGNORE_STACKTRACE).")
                        self.waiting_for_click = False
                    else:
                        self.waiting_for_click = True
                        preview = current_clipboard[:PREVIEW_CHARS]
                        more = '...' if len(current_clipboard) > PREVIEW_CHARS else ''
                        print(f"\n✅ Text copied (len={len(current_clipboard)}): {preview}{more}")
                        if REQUIRE_HOTKEY:
                            print(f"🔒 Hotkey mode: press {HOTKEY} to paste (clicks are ignored).")
                        else:
                            print("👆 Click in any application window to auto-type this text...")
                
                time.sleep(CLIPBOARD_CHECK_INTERVAL)
            except Exception as e:
                print(f"Error monitoring clipboard: {e}")
                time.sleep(CLIPBOARD_CHECK_INTERVAL)
    
    def on_click(self, x, y, button, pressed):
        """Handle mouse click events"""
        # Only respond to clicks when hotkey mode is disabled
        if not REQUIRE_HOTKEY and pressed and self.waiting_for_click and getattr(button, 'name', '') == 'left':
            # Small delay to ensure click is registered
            time.sleep(0.1)

            # Type the clipboard content
            print(f"⌨️  Typing at position ({x}, {y})...")
            try:
                # Use pyautogui to type the text
                pyautogui.write(self.clipboard_text, interval=TYPING_DELAY)
                print("✅ Text typed successfully!")
                self.waiting_for_click = False
            except Exception as e:
                print(f"❌ Error typing text: {e}")
    
    def start(self):
        """Start the paste typer"""
        print("=" * 60)
        print("🚀 Auto Paste Typer Tool")
        print("=" * 60)
        print("\nInstructions:")
        print("1. Enter the text you want to auto-type (end input with a single line containing only a dot '.')")
        print("2. Switch to the target application and left-click where you want the text to appear")
        print("3. The text will be automatically typed at the clicked position")
        print("4. Press ESC in this console to exit\n")

        # Ask the user for the text to type (support multi-line)
        print("Enter text (finish input with a single line containing only a dot '.'): ")
        lines = []
        try:
            while True:
                line = input()
                if line.strip() == '.':
                    break
                lines.append(line)
        except EOFError:
            pass

        text_to_type = '\n'.join(lines).rstrip('\n')
        if not text_to_type:
            print("No text entered — exiting.")
            return

        # Set the text that will be typed on click
        self.clipboard_text = text_to_type
        self.waiting_for_click = True

        print(f"\nText accepted (len={len(self.clipboard_text)}). Now click in the target app to type.")
        
        try:
            # Use pynput for mouse click detection
            from pynput import mouse

            # Start mouse listener (click-to-type mode)
            mouse_listener = mouse.Listener(on_click=self.on_click)
            mouse_listener.start()

            # If hotkey mode is enabled, register a hotkey to trigger typing
            if REQUIRE_HOTKEY:
                def do_type():
                    if self.waiting_for_click and self.clipboard_text:
                        print("⌨️  Hotkey triggered — typing clipboard text...")
                        try:
                            pyautogui.write(self.clipboard_text, interval=TYPING_DELAY)
                            print("✅ Text typed successfully!")
                            self.waiting_for_click = False
                        except Exception as e:
                            print(f"❌ Error typing text: {e}")

                try:
                    keyboard.add_hotkey(HOTKEY, do_type)
                    print(f"Hotkey registered: {HOTKEY} (press to paste). Press ESC to exit.")
                except Exception:
                    print(f"⚠️  Could not register hotkey {HOTKEY}. Falling back to click mode.")
                    if mouse_listener is None:
                        mouse_listener = mouse.Listener(on_click=self.on_click)
                        mouse_listener.start()

            # Wait for ESC key - use keyboard library or keep running until interrupted
            try:
                keyboard.wait('esc')
            except Exception as e:
                # If keyboard library fails, use input() instead
                print(f"Note: Using alternative exit method (keyboard lib issue: {e})")
                print("Press Enter to exit...")
                input()
            
            self.is_running = False
            mouse_listener.stop()
            print("\n\n👋 Program stopped. Goodbye!")
            
        except ImportError as e:
            print(f"❌ Error: Required library not installed: {e}")
            print("Please install it using: pip install -r requirements.txt")
            sys.exit(1)
        except KeyboardInterrupt:
            self.is_running = False
            print("\n\n👋 Program stopped. Goodbye!")

if __name__ == "__main__":
    # Disable pyautogui failsafe (optional, removes the safety feature)
    # pyautogui.FAILSAFE = False
    
    typer = PasteTyper()
    typer.start()

