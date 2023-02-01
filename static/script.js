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

touchpad.addEventListener("touchstart", function(e)
{
  e.preventDefault();
  last_touch = e.targetTouches.item(e.targetTouches.length - 1);
  start_touch = [last_touch.clientX, last_touch.clientY];
  if (e.targetTouches.length == 1)
  {
    send({"event": "touchstart", "pos": start_touch});
  }
  else
  {
    send({"event": "scrollstart", "pos": start_touch});
  }
});

touchpad.addEventListener("touchmove", function(e)
{
  e.preventDefault();
  last_touch = e.targetTouches.item(e.targetTouches.length - 1);
  new_touch = [last_touch.clientX, last_touch.clientY];
  send({"event": "touchmove", "pos": new_touch});
});

touchpad.addEventListener("touchend", function(e)
{
  send({"event": "touchend"});
});

touchpad.addEventListener("touchcancel", function(e)
{
  send({"event": "touchend"});
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

hidden_text_field.addEventListener("input", function(e)
{
  data = {"event": "input", "data": e.data};
  send(data);
});

hidden_text_field.addEventListener("keydown", function(e) {
  data = {"event": "key_down", "key": e.key};
  send(data);
});
