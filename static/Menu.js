document.getElementById("menu_shutdown").addEventListener("click", function(e)
{
  e.preventDefault();
  if (confirm("Ben je zeker?"))
  {
    window.open("shutdown", "_self");
    rpz_sender = new Sender(devices["RaspberryPiZero"]["host"]);
    rpz_sender.send({"event": "shutdown"});
  }
});