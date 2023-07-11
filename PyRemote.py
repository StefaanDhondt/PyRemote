from flask import Flask, render_template, request
from flask_sock import Sock
import json, os
from Utils import shutdown

app = Flask(__name__)
app.config.from_file("config.json", load=json.load)
devices = app.config["DEVICES"]
remotes = app.config["REMOTES"]
sock = Sock(app)

@app.route("/", methods=['GET'])
def home():
  return render_template(remotes[0]["template"], devices=devices, remotes=remotes, current_remote_index=0)

@app.route("/Remote", methods=['GET'])
def Remote():
   current_remote_index = int(request.args.get('remote_index'))
   return render_template(remotes[current_remote_index]["template"], devices=devices, remotes=remotes, current_remote_index=current_remote_index)

@app.route("/shutdown", methods=['GET'])
def shutdown_route():
  return render_template('Shutdown.html')

if os.name == 'nt':
  from WinUtils import handle_events as handle_win_events

  @sock.route('/win_events')
  def win_events(sock):
     handle_win_events(sock)

if os.name == 'posix': # Assumed raspberry pi
  from IRUtils import handle_events as handle_ir_events

  @sock.route('/ir_events')
  def ir_events(sock):
    handle_ir_events(sock, app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False, use_reloader=False, threaded=True)