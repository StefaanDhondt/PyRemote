# Wiring kaku

Using internal pin numbering (1 -> 40)

transmitter:
sig: pin 11 (GPIO17)
vcc: pin 2 (5V)
gnd: pin 9 (Ground)

receiver:
sig: pin 13 (GPIO27)
vcc: pin 1 (3.3V)
gnd: pin 6 (Ground)

# Wiring somfy

up: pin 36 (GPIO) green
down: pin 38 (GPIO20) blue
ch: pin 40 (GPIO21) black
vcc: pin 1 (3.3V) red
gnd: pin 39 (Ground) red

# Wiring IR
gnd: pin 6 (Ground) black
sig: pin 15 (GPIO22) yellow
vcc: pin 2 (5V) red/anode

# Power button
https://www.youtube.com/watch?v=wVnMZ4DXDNo
pin 5 and 6

# Power led
https://www.youtube.com/watch?v=B2SN_BF4MRQ
gnd: pin 6
sig: pin 8 (TXD)

duplicates:
pin 6 (gnd) 4x
pin 1: 3.3v 2x
pin 2: 5v 2x
