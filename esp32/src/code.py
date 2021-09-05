import board
import time
import wifi
import neopixel
import ipaddress
import socketpool
from digitalio import DigitalInOut, Direction

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets not found in secrets.py")
    raise

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True;
pixel_pin = board.NEOPIXEL
pixel_num = 50

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.1, auto_write=False)
pixels.fill((0, 0, 0))
pixels.show()

print("Connecting to %s..." % secrets["ssid"])
print("MAC: ", [hex(i) for i in wifi.radio.mac_address])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s, IPv4 Addr: " % secrets["ssid"], wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
socket = pool.socket()
socket.bind(['0.0.0.0', 80])
socket.listen(1)

print('Listening on 0.0.0.0:80')

while True:
    pixels.fill((16, 64, 128))
    pixels.show()
    print("Pixels enabled.")

    new_socket, remote_address = socket.accept()
    print("Received request from:", remote_address)
    buffer = bytearray(1024)
    new_socket.recv_into(buffer, 1024)
    print("Request:", buffer)

    pixels.fill((128, 64, 128))
    pixels.show()

    new_socket.send("SUCCESS!\r\n")
    new_socket.close()
