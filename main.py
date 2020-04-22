import board
import busio
import digitalio
import adafruit_rfm9x

# Set debug on and off
DEBUG = False

# Define radio parameters
RADIO_FREQ_MHZ = 915.0  # Define operating frequency

# Define board pins
CS = digitalio.DigitalInOut(board.RFM9X_CS)
RESET = digitalio.DigitalInOut(board.RFM9X_RST)

# Define the onboard LED
LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT

# Initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

# Set trasmit power
rfm9x.tx_power = 22

print("Waiting for packets...") # print to console
packet_count = 0;

while True:
    try:
        packet = rfm9x.receive(timeout=5.0) # default is .5 seconds unless specified, None is return if fail
        packet_count += 1 # Increment packet count

        if packet is None: # No packet received
            LED.value = False
            print("Received nothing. Packet count {0}".format(packet_count))
        else:
            # Received a packet
            LED.value = True

            if DEBUG:
                # Print out the raw bytes of the packet:
                print("Received (raw bytes): {0}".format(packet)) # Debug

            packet_text = str(packet, "ascii") # convert to ascii
            node_id = packet_text[0:3] # first 3 character, the node
            node_message = packet_text[3:] # from 3 characters on, the message

            print("Received message: \"{0}\" from node {1}".format(node_message, node_id)) # print to console

            rssi = rfm9x.rssi # Read RSSI for debug
            print("Received signal strength: {0} dB".format(rssi)) # print to console
    except UnicodeError:
        print("A unicode error caught") # catching malformed bytes from another transmitter
