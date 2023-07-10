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


def handle_events(sock, app):
  while True:
    data = sock.receive()
    req = json.loads(data)
    app.logger.warning(req)
    if req["event"] == "button_down":
      send_once(req["remote"], req["code"])
    elif req["event"] == "shutdown":
      os.system("shutdown /s /t 1")