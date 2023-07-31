sudo apt update

#############################
# Install & configure lirc
#############################
sudo apt install lirc
cd /etc/
sudo cp modules modules.bak

echo "Add following lines to the bottom of the /etc/modules file:"
echo "lirc_dev"
echo "lirc_rpi gpio_in_pin=23 gpio_out_pin=22"
sudo nano modules

cd /boot
sudo cp config.txt config.txt.bak

echo "Then add on line 51 of config.txt:"
echo "dtoverlay=gpio-ir-tx,gpio_pin=22"
sudo nano config.txt

sudo cp ~/PyRemote/PySetup/hardware.conf /etc/lirc/hardware.conf

cd /etc/lirc
sudo cp lirc_options.conf lirc_options.conf.bak
echo "Update line 11 of lirc_options.conf from"
echo "driver = devinput"
echo "to"
echo "driver=default"
sudo nano lirc_options.conf

sudo shutdown -r now

cd /etc/lirc/lircd.conf.d/
sudo wget -O PhilipsTV.conf https://sourceforge.net/p/lirc-remotes/code/ci/master/tree/remotes/philips/32PFL5403D-12.lircd.conf?format=raw
sudo wget -O OnkyoReceiver.conf https://sourceforge.net/p/lirc-remotes/code/ci/master/tree/remotes/onkyo/RC-735M.lircd.conf?format=raw

sudo systemctl stop lircd
sudo systemctl start lircd

#############################
# Install & configure PyRemote
#############################
sudo apt install git
sudo apt install python3-pip
sudo apt install python3-venv
pip install --upgrade pip
sudo pip install prun

cd ~
git clone https://StefaanDhondt@github.com/StefaanDhondt/PyRemote.git
cd PyRemote
python -m venv .venv
.venv/bin/pip install -r requirements.txt

chmod u+x PyRemote/run.sh

#############################
# Autostart PyRemote
#############################
sudo cp ~/PyRemote/PySetup/PyRemote.service /lib/systemd/system/PyRemote.service
sudo systemctl daemon-reload
sudo systemctl enable PyRemote
sudo shutdown -r now

#############################
# Install pihole
#############################
# Accept all questions except static IP one (should already be set in the router).
curl -sSL https://install.pi-hole.net | bash