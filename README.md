# Auto Paste Typer Tool

A Windows tool that automatically types clipboard content when you click in another application window.

## Features

- ✅ Monitors clipboard for changes
- ✅ Auto-types text when you click in any application
- ✅ Works with any Windows application
- ✅ Simple keyboard shortcut to exit (ESC)

## Installation

1. Make sure you have Python 3.7+ installed
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the program:
   ```bash
   python paste_typer.py
   ```

2. Copy text using `Ctrl+C` (or right-click → Copy)

3. Click anywhere in another application window (where you want the text to appear)

4. The text will be automatically typed at the cursor position

5. Press `ESC` to exit the program

## How It Works

1. The program continuously monitors your clipboard
2. When you copy new text, it stores it and waits for a mouse click
3. When you click in another application, it types the stored text at that position
4. You can repeat steps 2-3 as many times as needed

## Notes

- Make sure the target application window is active/visible
- The tool types character by character, so it may take a moment for long texts
- Works best when the target application has focus

## Troubleshooting

If you get permission errors, you may need to run as administrator on Windows.

