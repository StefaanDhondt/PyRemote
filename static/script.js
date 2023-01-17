function log(msg) {
  const container = document.getElementById("log");
  container.textContent = `${msg} \n${container.textContent}`;
}

var start_touch = null;
var new_touch = null;
var start_cursor = null;

const socket = new WebSocket('ws://' + location.host + '/events');

function send(input) {
  input_as_string = JSON.stringify(input);
  //log("Sending " + input_as_string);
  socket.send(input_as_string);
}

let touchpad = document.getElementById("touchpad");  

touchpad.addEventListener("touchstart", function(e)
{
  e.preventDefault();
  first_touch = e.touches.item(0);
  start_touch = [first_touch.clientX, first_touch.clientY];
  send({"event": "touchstart", "pos": start_touch});
});

touchpad.addEventListener("touchmove", function(e)
{
  e.preventDefault();
  first_touch = e.touches.item(0);
  new_touch = [first_touch.clientX, first_touch.clientY];
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
  data = {"event": "left_click_down"};
  send(data);
});

left_click.addEventListener("touchend", function(e) 
{
  data = {"event": "left_click_up"};
  send(data);
});

let right_click = document.getElementById("right_click");
right_click.addEventListener("touchstart", function(e) 
{
  data = {"event": "right_click_down"};
  send(data);
});

right_click.addEventListener("touchend", function(e) 
{
  data = {"event": "right_click_up"};
  send(data);
});

let keyboard = document.getElementById("keyboard");
let hidden_text_field = document.getElementById("hidden_text_field");

keyboard.addEventListener("click", function(e)
{
  hidden_text_field.focus();
  hidden_text_field.click();
});

hidden_text_field.addEventListener("input", function(e)
{
  log("input event" + e.data);
  data = {"event": "input", "data": e.data};
  send(data);
});

hidden_text_field.addEventListener("keydown", function(e) {
  log("keydown event" + e.key);
  data = {"event": "key_down", "key": e.key};
  send(data);
});
