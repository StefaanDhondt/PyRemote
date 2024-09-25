# Need to run this once:
# sudo apt-get install python3-rpi-lgpio
# otherwise:
# Traceback (most recent call last):
#   File "/usr/local/bin/listen-for-shutdown.py", line 9, in <module>
#     GPIO.wait_for_edge(3, GPIO.FALLING)
# RuntimeError: Error waiting for edge

sudo cp listen-for-shutdown.py /usr/local/bin/
sudo chmod +x /usr/local/bin/listen-for-shutdown.py

sudo cp listen-for-shutdown.sh /etc/init.d/
sudo chmod +x /etc/init.d/listen-for-shutdown.sh

sudo update-rc.d listen-for-shutdown.sh defaults