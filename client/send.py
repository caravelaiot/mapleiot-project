#!/usr/bin/python3

import time
import board
import busio
import digitalio
import adafruit_rfm9x

# Configurable globals
NODE_RADIO_FREQ_MHZ = 915.0  # Frequency transmission
NODE_ID = 22 
NODE_MESSAGE = "test" # This normally would be a sensor value

# Define pins connected to the chip.
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)

# Initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, NODE_RADIO_FREQ_MHZ)
rfm9x.tx_power = 23

def sendMessage(nid, message):
    nid = str(nid).zfill(3) # Pad the NODE_ID so it's always 3 characters
    rfm9x.send(bytes("{0}{1}".format(nid, message), "UTF-8"))

sendMessage(NODE_ID, NODE_MESSAGE)

