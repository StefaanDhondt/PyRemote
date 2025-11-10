function add_keyboard_event_listeners(button, text_field, sender)
{
  add_keyboard_event_listeners.keyboard_visible = false;
  
  button.addEventListener("click", function(e)
  {
    if (!add_keyboard_event_listeners.keyboard_visible)
    {
      hidden_text_field.focus();
      hidden_text_field.click();
    }
    add_keyboard_event_listeners.keyboard_visible = !add_keyboard_event_listeners.keyboard_visible;
  });

  text_field.addEventListener("input", function(e)
  {
    // On Windows Phone/Edge, an input event is emitted when
    // a key is pressed, as well as a keydown event. So to avoid
    // processing the key twice, we don't process it here.
    // We reserve this event for sending a string.
    //if (e.data.length > 1)
    {
      sender.send({"event": "input", "data": e.data});
    }
  });
  
  document.addEventListener("keydown", function(e)
  {
    sender.send({"event": "key_down", "key": e.key});
  });
}