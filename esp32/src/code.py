import board
import wifi
import neopixel
import socketpool
from digitalio import DigitalInOut, Direction
import ampule

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

@ampule.route("/led_on")
def led_on(request):
    pixels.fill((128, 64, 128))
    pixels.show()
    return (200, {"content-type": "application/json"}, '{success: true}')

@ampule.route("/led_off")
def led_on(request):
    pixels.fill(0)
    pixels.show()
    return (200, {"content-type": "application/json"}, '{success: true}')

pixels.fill((16, 64, 128))
pixels.show()
print("Pixels enabled.")

while True:
    client, remote_address = socket.accept()
    print("Received request from:", remote_address)
    request = ampule.get_request(client)
    if request:
        (method, path, params, headers, data) = request
        print("Matching path: %s" % path)
        match = ampule.match_route(path)
        if match:
            args, route = match
            status, headers, body = route["func"](request, *args)

    ampule.send_response(client, status, headers, body)
