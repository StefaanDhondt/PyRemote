from Utils import run_command
import json
import os

def send_once(remote, code):
  command = f"irsend send_once {remote} {code}"
  run_command(command.split(" "))


def handle_events(sock, app):
  while True:
    data = sock.receive()
    req = json.loads(data)
    if req["event"] == "button_down":
      send_once(req["remote"], req["code"])
    elif req["event"] == "shutdown":
      os.system("sudo shutdown now")