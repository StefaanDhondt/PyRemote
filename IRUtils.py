from Utils import run_command
import json
import os
from screens import ScreenRemote

def send_once(remote, code):
  command = f"irsend send_once {remote} {code}"
  run_command(command.split(" "))


def handle_events(sock, app):
  while True:
    data = sock.receive()
    req = json.loads(data)
    if req["event"] == "button_down":
      if req["remote"] == "somfy":
        button, channel_str = req["button"].split("_")
        channel = int(channel_str)
        sr = ScreenRemote()
        if button == "down":
          sr.down(channel)
        elif button == "up":
          sr.up(channel)
      else:
        send_once(req["remote"], req["code"])
    elif req["event"] == "shutdown":
      os.system("sudo shutdown now")
