function log(msg)
{
  const container = document.getElementById("log");
  container.textContent = `${msg} \n${container.textContent}`;
}

var start_touch = null;
var new_touch = null;
var start_cursor = null;
var socket = null; 
var queue = []

function send(input) 
{
  input_as_string = JSON.stringify(input);
  if (!socket || socket.readyState !== WebSocket.OPEN) 
  {
    queue.push(input_as_string);
    if (!socket || socket.readyState !== WebSocket.CONNECTING)
    {
      socket = new WebSocket('ws://' + location.host + '/events');
      socket.onopen = function()
      {
        while (queue.length > 0) 
        {
          socket.send(queue.pop());
        }
      }
    }
  } 
  else 
  {
    socket.send(input_as_string)
  }
}

let touchpad = document.getElementById("touchpad");  
let touch_pos_anchor;

touchpad.addEventListener("touchstart", function(e)
{
  e.preventDefault();
  last_touch = e.targetTouches.item(e.targetTouches.length - 1);
  touch_pos_anchor = [last_touch.clientX, last_touch.clientY];
  if (e.targetTouches.length == 1)
  {
    send({"event": "mouse_move_begin"});
  }
  else
  {
    send({"event": "scroll_begin"});
  }
});

touchpad.addEventListener("touchmove", function(e)
{
  e.preventDefault();
  last_touch = e.targetTouches.item(e.targetTouches.length - 1);
  touch_pos_delta = [(last_touch.clientX - touch_pos_anchor[0]) * 2, 
                     (last_touch.clientY - touch_pos_anchor[1]) * 2];
  send({"event": "mouse_move", "delta": touch_pos_delta});
});

touchpad.addEventListener("touchend", function(e)
{
  send({"event": "mouse_move_end"});
});

touchpad.addEventListener("touchcancel", function(e)
{
  send({"event": "mouse_move_end"});
});

let left_click = document.getElementById("left_click");
left_click.addEventListener("touchstart", function(e) 
{
  this.style.backgroundColor = "lightgray";
  send({"event": "left_click_down"});
});

left_click.addEventListener("touchend", function(e) 
{
  this.style.backgroundColor = "white";
  send({"event": "left_click_up"});
});


let right_click = document.getElementById("right_click");
right_click.addEventListener("touchstart", function(e) 
{
  this.style.backgroundColor = "lightgray";
  send({"event": "right_click_down"});
});

right_click.addEventListener("touchend", function(e) 
{
  this.style.backgroundColor = "white";
  send({"event": "right_click_up"});
});

document.getElementById("esc").addEventListener("click", function(e)
{
  send({"event": "key_down", "key": "escape"});
});

document.getElementById("playpause").addEventListener("click", function(e)
{
  send({"event": "key_down", "key": "playpause"});
});

document.getElementById("voldown").addEventListener("click", function(e)
{
  send({"event": "key_down", "key": "voldown"});
});

document.getElementById("volup").addEventListener("click", function(e)
{
  send({"event": "key_down", "key": "volup"});
});

let keyboard = document.getElementById("keyboard");
let keyboard_visible = false;
let hidden_text_field = document.getElementById("hidden_text_field");

keyboard.addEventListener("click", function(e)
{
  if (!keyboard_visible)
  {
    hidden_text_field.focus();
    hidden_text_field.click();
  }
  keyboard_visible = !keyboard_visible;
});

document.getElementById("shutdown").addEventListener("click", function(e)
{
  send({"event": "shutdown"});
});

hidden_text_field.addEventListener("input", function(e)
{
  // On Windows Phone/Edge, an input event is emitted when
  // a key is pressed, as well as a keydown event. So to avoid
  // processing the key twice, we don't process it here.
  // We reserve this event for sending a string.
  if (e.data.length > 1)
  {
    send({"event": "input", "data": e.data});
  }
});

document.addEventListener("keydown", function(e)
{
  send({"event": "key_down", "key": e.key});
});
