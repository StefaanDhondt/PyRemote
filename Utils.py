import sys, os

def shutdown():
  if sys.platform == 'win32':
    os.system("shutdown /s /t 1")
  else:
    os.system('sudo shutdown now')