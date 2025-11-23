"""
Quick check to verify all dependencies are installed correctly.
Run this to test if your Python environment is set up correctly.
"""

import sys

print("Python version:", sys.version)
print("Python executable:", sys.executable)
print("\nChecking required packages...\n")

packages = ['pyperclip', 'pyautogui', 'keyboard', 'pynput']
missing = []

for package in packages:
    try:
        __import__(package)
        print(f"✅ {package} - installed")
    except ImportError:
        print(f"❌ {package} - MISSING")
        missing.append(package)

if missing:
    print(f"\n❌ Missing packages: {', '.join(missing)}")
    print(f"\nTo install, run:")
    print(f"  python -m pip install {' '.join(missing)}")
    sys.exit(1)
else:
    print("\n✅ All packages are installed correctly!")
    print("You can now run: python paste_typer.py")

