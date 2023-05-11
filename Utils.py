import sys, os
from subprocess import call

def shutdown():
  if sys.platform == 'win32':
    os.system("shutdown /s /t 1")
  else:
    os.system('sudo shutdown now')

def run_command(command):
    print("command:", command)

    call_value = call(command, stdout=sys.stdout, stderr=sys.stdout)

    if call_value != 0:
        print("Command failure.")
        sys.stdout.flush()
        sys.exit(1)