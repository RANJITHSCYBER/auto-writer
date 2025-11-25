# Auto Writer — Fast Text Automation Tool

A lightweight Windows desktop application that automatically types text into any target application. Perfect for automation, data entry, and repetitive typing tasks.

## Features

✨ **High-Speed Typing** — Configurable character-by-character typing with speed control (1–300 ms per keystroke)

🎯 **Click-to-Target** — Click anywhere on your screen to select where typing begins; GUI minimizes for clean interaction

⏸️ **ESC to Stop** — Press ESC at any time to stop typing mid-operation

🔒 **Safe & Reliable** — Detects and focuses the target window before typing; avoids typing into wrong applications

⚡ **Simple GUI** — Minimalist Tkinter interface with text input, speed slider, and status feedback

🚀 **No Dependency on Clipboard** — Uses direct keyboard simulation for faster, more reliable insertion

## Requirements

- **Windows 10+** (uses Windows API for window detection and focus)
- **Python 3.8+**

## Quick Start

### 1. Install Dependencies

```powershell
pip install pynput pyautogui
```

### 2. Run the GUI

```powershell
python paste_gui_simple.py
```

### 3. Use It

1. Enter text in the text box
2. Click `Start (click target)`
3. Click in the target application where you want typing to begin
4. Text types automatically at your chosen speed
5. Press **ESC** to stop anytime

## Detailed Usage

### Speed Control

The slider adjusts delay **per keystroke** in milliseconds:
- **1–10 ms** — Maximum speed (very fast, may miss keys in slow apps)
- **30 ms** (default) — High speed, reliable for most applications
- **100+ ms** — Slower, suitable for sensitive fields or lagging applications

### Window Detection

The tool automatically:
- Detects which window is under your click
- Brings it to foreground
- Waits for focus to settle
- Releases any held modifier keys
- Begins typing

### Stop Anytime

Press **ESC** at any time during typing to cancel the operation immediately.

## Configuration

### Manual Focus Delay Adjustment

If typing appears in the GUI instead of your target, increase the focus delay:

Edit `paste_gui_simple.py` and change:
```python
time.sleep(0.15)  # Current (150 ms)
```
to:
```python
time.sleep(0.25)  # Try this (250 ms)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Typing in wrong window | Ensure GUI is minimized before clicking target; increase focus delay |
| Keystrokes missed/dropped | Move speed slider right (increase delay per keystroke) |
| Cannot type into UAC/Admin prompts | Windows blocks synthetic input into elevated windows |
| Cannot type into Remote Desktop | Run locally; RDP may restrict keyboard automation |
| ESC doesn't stop immediately | Threading delay; give it 1–2 seconds |
| "pynput not found" error | Run: `pip install pynput` |
| "pyautogui not found" error | Run: `pip install pyautogui` |

## Project Files

```
├── paste_gui_simple.py      ← Main GUI (recommended, start here)
├── paste_gui.py             ← Full-featured GUI with preview (optional)
├── paste_server.py          ← Flask server for remote automation (optional)
├── paste_typer.py           ← Core automation engine
├── requirements.txt         ← Dependency list
└── README.md                ← This file
```

## Optional: Server Mode

For headless or remote automation:

```powershell
# Install Flask
pip install flask

# Run server
python paste_server.py
```

Then POST to the local endpoint:

```bash
curl -X POST http://localhost:8765/auto-type \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World"}'
```

## Performance & Speed

Typical typing rates:
- **30 ms/key** → ~33 keys/sec (default, balanced)
- **10 ms/key** → ~100 keys/sec (fast, test first)
- **1 ms/key** → Maximum (risky; may drop keystrokes)

## Security & Privacy

- **Local Only** — Operates entirely on your machine; no cloud or remote servers
- **No Logging** — Typed text is never saved or logged
- **Optional Server Auth** — If using server mode, set `AUTO_WRITER_SECRET` environment variable
- **Open Source** — Full code transparency

## Legal & Ethical Use

This tool is for:
- ✅ Personal productivity and automation
- ✅ Accessibility assistance
- ✅ Data entry automation in your own applications
- ✅ Development and testing

This tool is **not** for:
- ❌ Bypassing security controls or authentication
- ❌ Unauthorized automation of third-party services
- ❌ Violation of terms of service
- ❌ Any illegal or harmful purpose

Users are responsible for compliant and ethical use.

## Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

## License

MIT License — Free for personal and commercial use

## Support

Found a bug or have a feature request?
- Open a GitHub Issue with:
  - Windows version
  - Python version (`python --version`)
  - Error message (if any)
  - Steps to reproduce

---

**Made for Windows automation, accessibility, and productivity. Happy typing! 🚀**

