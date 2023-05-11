from Utils import run_command
import json

def send_start(remote, code):
  command = f"irsend send_start {remote} {code}"
  #run_command(command.split(" "))

def send_stop(remote, code):
  command = f"irsend send_stop {remote} {code}"
  #run_command(command.split(" "))

def send_once(remote, code):
  command = f"irsend send_once {remote} {code}"
  run_command(command.split(" "))


def handle_events(sock):
  while True:
    data = sock.receive()
    req = json.loads(data)
    if req["event"] == "button_down":
      send_start(req["remote"], req["code"])
    #elif req["event"] == "button_up":
    #  send_stop(req["remote"], req["code"])
