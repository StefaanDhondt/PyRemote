



git clone https://github.com/joostfra68/rpi433.git
cd rpi433/
chmod +x build.sh
./build.sh
./rpi433receive
# output for light veranda:
# Addr 7925131 unit 1 on, period: 254 us.
# Addr 7925131 unit 1 off, period: 254 us.

./rpi433send 7925131 1 on
./rpi433send 7925131 1 off

# output for light zolder:
# Addr 7922683 unit 1 on, period: 255 us.
# Addr 7922683 unit 1 off, period: 256 us. 

./rpi433send 7922683 1 on
./rpi433send 7922683 1 off

# output for light Margo:
# Addr 17307830 unit 10 off, period: 244 us. 
# Addr 17307830 unit 10 on, period: 244 us.

./rpi433send 17307830 10 on
./rpi433send 17307830 10 off
