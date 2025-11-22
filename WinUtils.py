import json, os
import win32api, win32con, win32service
from ctypes import windll

PIXEL_TOLERANCE = 2

def generate_key_up_down_events(key, shift=False):
    if shift:
      win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(key, 0, 0, 0)
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

def handle_events(sock):
  anchor_cursor_pos = None
  scrolling = False
  scroll_pos = 0
  while True:
    data = sock.receive()
    req = json.loads(data)
    hdesk = win32service.OpenInputDesktop(0, False, win32con.MAXIMUM_ALLOWED)
    hdesk.SetThreadDesktop()

    if req["event"] == "mouse_move_begin":
      anchor_cursor_pos = win32api.GetCursorPos()
    elif req["event"] == "scroll_begin":
      anchor_cursor_pos = win32api.GetCursorPos()
      scrolling = True
      scroll_pos = 0
    elif req["event"] == "mouse_move":
      if anchor_cursor_pos:
        delta = req["delta"]        
        if scrolling:
          expected_scroll_pos = -delta[1]
          scroll_update = int(expected_scroll_pos - scroll_pos)
          win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, scroll_update, 0)
          scroll_pos = expected_scroll_pos
        else:
          x = anchor_cursor_pos[0] + delta[0]
          y = anchor_cursor_pos[1] + delta[1]
          screen_width = win32api.GetSystemMetrics(0)
          screen_height = win32api.GetSystemMetrics(1)
          factor = 65535.0
          win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, int(x * factor / screen_width), int(y * factor / screen_height))
    elif req["event"] == "mouse_move_end":
      if not scrolling:
        if anchor_cursor_pos:
          cursor_pos = win32api.GetCursorPos()
          if (abs(anchor_cursor_pos[0] - cursor_pos[0]) + abs(anchor_cursor_pos[1] - cursor_pos[1])) <= PIXEL_TOLERANCE:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)  
      anchor_cursor_pos = None
      scrolling = False
    elif req["event"] == "input":
      if ("data" in req):
        generate_keyboard_events(req["data"])
    elif req["event"] == "key_down":
      if req["key"] == "Backspace":
        generate_key_up_down_events(win32con.VK_BACK)
      elif req["key"] == "Enter":
        generate_key_up_down_events(win32con.VK_RETURN)
      elif req["key"] == "escape":
        generate_key_up_down_events(win32con.VK_ESCAPE)
      elif req["key"] == "playpause":
        generate_key_up_down_events(win32con.VK_MEDIA_PLAY_PAUSE)
      elif req["key"] == "voldown":
        generate_key_up_down_events(win32con.VK_VOLUME_DOWN)
      elif req["key"] == "volup":
        generate_key_up_down_events(win32con.VK_VOLUME_UP)
      elif len(req["key"]) == 1: 
        # If "key" is a single character, we assume it doesn't have to be 
        # converted/translated.
        generate_keyboard_events(req["key"])
      else:
        # We don't know this key, so just print it.
        print(req["key"])
    elif req["event"] == "left_click_down":
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    elif req["event"] == "left_click_up":
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    elif req["event"] == "right_click_down":
      win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    elif req["event"] == "right_click_up":
      win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
    elif req["event"] == "power":
      os.system("shutdown /s /t 0")
