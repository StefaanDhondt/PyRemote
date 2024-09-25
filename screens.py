

from time import sleep, time
import RPi.GPIO as GPIO
from pathlib import Path

class ScreenRemote:
  def __init__(self):
    self.buttons = {
      "UP": 36,
      "DOWN": 38,
      "CH": 40
    }

    self.file = "somfy-channel.ch"

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

    # If up or down was pressed, the channel button is sleeping.
    if button_idx in [self.buttons["UP"], self.buttons["DOWN"]]:
      # Set the time of the last press to 0 such that the `switch_to_channel` 
      # function will conclude that the remote is asleep.
      ScreenRemote.switch_to_channel.time_last_press = 0.0

    print(f"Button {name} pressed.")

  def get_current_channel(self):
    with open(self.file, "r") as file:
      return int(file.read())

  def set_current_channel(self, channel):
    with open(self.file, "w") as file:
      file.write(str(channel))

  def switch_to_channel(self, channel):
    if channel < 0 or channel > 4:
      raise Exception(f"Invalid channel {channel} (Should be within [0, 4])")

    current_channel = self.get_current_channel()
    print(f"Current channel: {current_channel}")

    if current_channel == channel:
      return

    nr_presses = (channel + 5 - current_channel) % 5
    print(f"Nr of presses: {nr_presses}")

    remote_asleep = True
    if hasattr(ScreenRemote.switch_to_channel, "time_last_press"):
      time_since_last_press = time() - ScreenRemote.switch_to_channel.time_last_press
      if time_since_last_press < 4.5:
        remote_asleep = False
      elif time_since_last_press < 5.5:
        print("The remote might be asleep, wait 1 sec. to make sure")
        sleep(1)

    if remote_asleep:
      print("The remote is asleep, wake it up with an extra button press.")
      nr_presses += 1

    for pi in range(nr_presses):
      self.press_button("CH")
    ScreenRemote.switch_to_channel.time_last_press = time()

    self.set_current_channel(channel)

  def up(self, channel):
    self.switch_to_channel(channel)
    self.press_button("UP")

  def down(self, channel):
    self.switch_to_channel(channel)
    self.press_button("DOWN")
