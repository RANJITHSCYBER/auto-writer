# VS Code Setup Instructions

If you're getting `ModuleNotFoundError` in VS Code, you need to select the correct Python interpreter.

## Steps to Fix:

1. **Open Command Palette** (Ctrl+Shift+P)

2. **Type**: `Python: Select Interpreter`

3. **Choose the Python interpreter** that shows version 3.12.0 (or the one where you installed the packages)

   - It should show something like: `Python 3.12.0 ('base': venv) c:\Users\...\python.exe`
   
4. **Alternatively**, you can also:
   - Click on the Python version in the bottom-right corner of VS Code
   - Select the correct interpreter from the list

5. **Verify installation** by running:
   ```
   python setup_check.py
   ```

6. **If packages are still missing**, install them using:
   ```
   python -m pip install pyperclip pyautogui keyboard pynput
   ```

## Quick Test:

Run this command in VS Code terminal (make sure you're in the project directory):
```bash
python setup_check.py
```

This will verify all packages are installed correctly.

