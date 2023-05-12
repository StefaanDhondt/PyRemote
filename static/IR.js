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
      socket = new WebSocket('ws://' + host + '/ir_events');
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
    socket.send(input_as_string);
  }
}

function handle_touch_event(e)
{
  last_touch = e.targetTouches.item(e.targetTouches.length - 1);
  send({ "event": "button_down", "remote": remote, "code": last_touch.target.id });
}

buttons = document.getElementById("buttons");
buttons.addEventListener("touchstart", handle_touch_event);