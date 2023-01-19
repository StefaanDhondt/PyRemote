from flask import Flask, render_template, request
import win32api
import win32con
import win32service
import json
from ctypes import windll
from flask_sock import Sock

def generate_key_up_down_events(key, shift=False):
    if shift:
      win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(key, 0, 0, 0)
    #time.sleep(0.05)
    win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
    if shift:
      win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)

def generate_keyboard_events(string):
  for char in string:
    # https://msdn.microsoft.com/en-us/library/windows/desktop/ms646329(v=vs.85).aspx
    res = windll.User32.VkKeyScanW(ord(char))
    shift = (res & 0xFF00) >> 8
    vk_key = res & 0xFF
    generate_key_up_down_events(vk_key, shift)

app = Flask(__name__)
sock = Sock(app)

@app.route("/", methods=['GET'])
def home():
  return render_template('index.html', host=request.host)


@sock.route('/events')
def handle_events(sock):
  anchor_touch_pos = None
  anchor_cursor_pos = None
  while True:
    data = sock.receive()
    req = json.loads(data)
    if req["event"] == "touchstart":
      anchor_touch_pos = req["pos"]
      anchor_cursor_pos = win32api.GetCursorPos()
    elif req["event"] == "touchmove":
      if anchor_touch_pos:
        curr_touch_pos = req["pos"]
        touch_delta = [curr_touch_pos[0] - anchor_touch_pos[0], curr_touch_pos[1] - anchor_touch_pos[1]]
        hdesk = win32service.OpenInputDesktop(0, False, win32con.MAXIMUM_ALLOWED);
        hdesk.SetThreadDesktop()
        win32api.SetCursorPos((int(anchor_cursor_pos[0] + touch_delta[0] * 2), int(anchor_cursor_pos[1] + touch_delta[1] * 2)))
        #if scrolling:
        #  if touch_delta[1] > 0:
        #    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -120, 0)
        #  else:          
        #    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, 120, 0)
    elif req["event"] == "touchend":
      if anchor_cursor_pos:
        if anchor_cursor_pos == win32api.GetCursorPos():
          win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
          win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)  
      anchor_touch_pos = None
      anchor_cursor_pos = None
    elif req["event"] == "touchcancel":
      anchor_touch_pos = None
      anchor_cursor_pos = None
    elif req["event"] == "input":
      if (req["data"]):
        generate_keyboard_events(req["data"])
    elif req["event"] == "key_down":
      if req["key"] == "Backspace":
        generate_key_up_down_events(win32con.VK_BACK)
      elif req["key"] == "Enter":
        generate_key_up_down_events(win32con.VK_RETURN)
    elif req["event"] == "left_click_down":
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    elif req["event"] == "left_click_up":
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    elif req["event"] == "right_click_down":
      win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    elif req["event"] == "right_click_up":
      win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)