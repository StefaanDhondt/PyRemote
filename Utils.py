import sys, os
from subprocess import call

def run_command(command):
    print("command:", command)

    call_value = call(command, stdout=sys.stdout, stderr=sys.stdout)

    if call_value != 0:
        print("Command failure.")
        sys.stdout.flush()
        sys.exit(1)