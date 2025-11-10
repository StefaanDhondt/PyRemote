from flask import Flask, render_template
from flask_sock import Sock
import os, socket

app = Flask(__name__)
sock = Sock(app)

def get_local_ip():
    try:
        # Connect to a remote address (doesn't actually send data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

@app.route("/", methods=['GET'])
def home():
  return render_template("WindowsPC.html", server_ip=get_local_ip())

if os.name == 'nt':
  from WinUtils import handle_events as handle_win_events

  @sock.route('/win_events')
  def win_events(sock):
     handle_win_events(sock)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False, use_reloader=False, threaded=True)