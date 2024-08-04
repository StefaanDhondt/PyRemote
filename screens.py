from time import sleep
import RPi.GPIO as GPIO

BUTTONS = {
    'UP': 36,
    'DOWN': 38,
    'CH': 40
}

class ScreenRemote:
  def __init__(self):
    self.buttons = {
      "UP": 36,
      "DOWN": 38,
      "CH": 40
    }

    try:
      GPIO.setwarnings(True)
      GPIO.setmode(GPIO.BOARD)
      for idx in self.buttons.values():
        GPIO.setup(idx, GPIO.OUT, initial=GPIO.HIGH)
    except RuntimeError as e:
      print("Error: {}".format(str(e)))
      sys.exit(1)

  def press_button(self, name):
    # Delay during which the given button remains pressed
    delay_press = 0.1

    button_idx = self.buttons[name]
    GPIO.output(button_idx, GPIO.LOW)
    sleep(delay_press)
    GPIO.output(button_idx, GPIO.HIGH)
    sleep(delay_press)
