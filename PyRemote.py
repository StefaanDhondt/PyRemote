from flask import Flask, render_template, request
from flask_sock import Sock
import json, os
from Utils import shutdown

app = Flask(__name__)
app.config.from_file("config.json", load=json.load)
devices = app.config["DEVICES"]
device_list = [{ "name": device[0], **device[1] } for device in devices.items()]
sock = Sock(app)

@app.route("/", methods=['GET'])
def home():
  return render_template('Template.html', devices=device_list, current_device=device_list[0])

@app.route("/Device", methods=['GET'])
def Device():
   current_device_name = request.args.get('device_name')
   current_device = { "name": current_device_name, **devices[current_device_name] }
   return render_template('Template.html', devices=device_list, current_device=current_device)

@app.route("/shutdown", methods=['GET'])
def shutdown_route():
  shutdown()
  return render_template('Shutdown.html')

if os.name == 'nt':
  from WinUtils import handle_events as handle_win_events

  @sock.route('/win_events')
  def win_events(sock):
     handle_win_events(sock)

if True: #os.name == 'posix': # Assumed raspberry pi
  from IRUtils import handle_events as handle_ir_events

  @sock.route('/ir_events')
  def ir_events(sock):
    handle_ir_events(sock, app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False, use_reloader=False, threaded=True)