import subprocess
import sys

# Install necessary packages
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'undetected-chromedriver'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'selenium'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygetwindow'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyautogui'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'beautifulsoup4'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'lxml'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pywin32'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'openpyxl'])