document.getElementById("menu_shutdown").addEventListener("click", function(e)
{
  e.preventDefault();
  if (confirm("Ben je zeker?"))
  {
    rpz_sender = new Sender(devices["RaspberryPiZero"]["host"]);
    rpz_sender.send({"event": "shutdown"});
  }
});