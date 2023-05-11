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

remote_buttons = document.getElementsByClassName("remote_button");

for (var i = 0; i < remote_buttons.length; i++)
{
  remote_button = remote_buttons[i];
  console.log(remote_button.id);
  remote_button.addEventListener("touchstart", function(e)
  {
    send({ "event": "button_down", "remote": remote, "code": remote_button.id });
  });
  remote_button.addEventListener("touchend", function(e)
  {
    send({ "event": "button_up", "remote": remote, "code": remote_button.id });
  });
}