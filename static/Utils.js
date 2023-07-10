class Sender
{
  constructor(host)
  {
    this.socket = new WebSocket('ws://' + host);
    //var ws = this;
    this.queue = []
    this.socket.onopen = function()
    {
      while (this.queue.length > 0) 
      {
        this.socket.send(this.queue.pop());
      }
    }.bind(this);
  }

  send(input)
  {
    let input_as_string = JSON.stringify(input);
    if (this.socket.readyState === WebSocket.OPEN)
    {
      this.socket.send(input_as_string);
    }
    else
    {
      this.queue.push(input_as_string);
    }
  }
}


function send_ir_event(remote, code, sender)
{
  sender.send({ "event": "button_down", "remote": remote, "code": code });
}