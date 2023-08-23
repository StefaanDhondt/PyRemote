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


#############################
# Mount stack media (webdav) at startup
#############################
sudo apt-get install davfs2 # A window to configure davfs2 will open, confirm with yes that unprivileged users should be able to mount WebDAV resources

sudo usermod -a -G davfs2 Stefaan

mkdir StackMedia
mkdir .davfs2

sudo cp /etc/davfs2/secrets /home/Stefaan/.davfs2/secrets
sudo chown Stefaan:Stefaan /home/Stefaan/.davfs2/secrets
sudo chmod 600 /home/Stefaan/.davfs2/secrets

echo "Add following line to the end of the file:"
echo "https://julesthegreat.stackstorage.com/remote.php/webdav/ media <webdav token>"
sudo nano /home/Stefaan/.davfs2/secrets

echo "Add following line to the end of the file:"
echo "https://julesthegreat.stackstorage.com/remote.php/webdav/ /home/Stefaan/StackMedia davfs user,rw,auto 0 0"
sudo nano /etc/fstab

# TOREMOVE:
#sudo mount.davfs https://julesthegreat.stackstorage.com/remote.php/webdav/ ~/StackMedia -o rw,uid=Stefaan

#############################
# Share mounted folder on the network
#############################
sudo apt-get install samba

echo "Scroll down and find the section named Authentication; change the # security = user line to security = user."
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak
sudo nano /etc/samba/smb.conf

sudo pdbedit -a -u Stefaan

sudo service smbd restart