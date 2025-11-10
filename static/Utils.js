class Sender
{
  constructor(host)
  {
    this.host = host;
    this.socket = null;
    this.queue = [];
  }

  send(input)
  {
    let input_as_string = JSON.stringify(input);
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) 
    {
      this.queue.push(input_as_string);
      if (!this.socket || this.socket.readyState !== WebSocket.CONNECTING)
      {
        this.socket = new WebSocket('ws://' + this.host);
        this.socket.onopen = function()
        {
          while (this.queue.length > 0) 
          {
            this.socket.send(this.queue.pop());
          }
        }.bind(this);
      }
    } 
    else 
    {
      this.socket.send(input_as_string);
    }  
  }
}