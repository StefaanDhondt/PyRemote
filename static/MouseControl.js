function add_touchpad_listeners(touchpad, sender)
{
  touchpad.addEventListener("touchstart", function(e)
  {
    e.preventDefault();
    last_touch = e.targetTouches.item(e.targetTouches.length - 1);
    add_touchpad_listeners.touch_pos_anchor = [last_touch.clientX, last_touch.clientY];
    if (e.targetTouches.length == 1)
    {
      sender.send({"event": "mouse_move_begin"});
    }
    else
    {
      sender.send({"event": "scroll_begin"});
    }
  });
  touchpad.addEventListener("touchmove", function(e)
  {
    e.preventDefault();
    last_touch = e.targetTouches.item(e.targetTouches.length - 1);
    touch_pos_delta = [(last_touch.clientX - add_touchpad_listeners.touch_pos_anchor[0]) * 2, 
                      (last_touch.clientY - add_touchpad_listeners.touch_pos_anchor[1]) * 2];
    sender.send({"event": "mouse_move", "delta": touch_pos_delta});
  });
  touchpad.addEventListener("touchend", function(e)
  {
    sender.send({"event": "mouse_move_end"});
  });
  touchpad.addEventListener("touchcancel", function(e)
  {
    sender.send({"event": "mouse_move_end"});
  });
}

function add_left_button_listeners(button, sender)
{
  button.addEventListener("touchstart", function(e) 
  {
    this.style.backgroundColor = "lightgray";
    sender.send({"event": "left_click_down"});
  });
  button.addEventListener("mousedown", function(e) 
  {
    this.style.backgroundColor = "lightgray";
    sender.send({"event": "left_click_down"});
  });  
  button.addEventListener("touchend", function(e) 
  {
    this.style.backgroundColor = "white";
    sender.send({"event": "left_click_up"});
  });
  button.addEventListener("mouseup", function(e) 
  {
    this.style.backgroundColor = "white";
    sender.send({"event": "left_click_up"});
  });
}

function add_right_button_listeners(button, sender)
{
  button.addEventListener("touchstart", function(e) 
  {
    this.style.backgroundColor = "lightgray";
    sender.send({"event": "right_click_down"});
  });
  button.addEventListener("mousedown", function(e) 
  {
    this.style.backgroundColor = "lightgray";
    sender.send({"event": "right_click_down"});
  });  
  button.addEventListener("touchend", function(e) 
  {
    this.style.backgroundColor = "white";
    sender.send({"event": "right_click_up"});
  });
  button.addEventListener("mouseup", function(e) 
  {
    this.style.backgroundColor = "white";
    sender.send({"event": "right_click_up"});
  });
}

function add_listeners(touchpad, left_button, right_button, sender)
{
  add_touchpad_listeners(touchpad, sender);
  add_left_button_listeners(left_button, sender);
  add_right_button_listeners(right_button, sender);
}