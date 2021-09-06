import board
import wifi
import neopixel
import socketpool
import io
import re
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

routes = []
variable_re = re.compile("^<([a-zA-Z]+)>$")

def get_request(client):
    try:
        client.setblocking(False)
        buffer = bytearray(1024)
        client.recv_into(buffer)
        reader = io.BytesIO(buffer)
    except OSError:
        return None

    line = str(reader.readline(), "utf-8")
    (method, full_path, version) = line.rstrip("\r\n").split(None, 2)
    path = full_path.split("?")[0]
    query_string = full_path.split("?")[1]

    param_list = query_string.split("&")
    params = {}
    for param in param_list:
        key_val = param.split("=")
        if len(key_val) == 2:
            params[key_val[0]] = key_val[1]

    headers = {}
    for line in reader:
        if line == b'\r\n': break
        header = str(line, "utf-8")
        title, content = header.split(":", 1)
        headers[title.strip().lower()] = content.strip()

    data = ""
    for line in reader:
        if line == b'\r\n': break
        data += str(line, "utf-8")

    return (method, path, params, headers, data)

def send_response(client, code, headers, data):
    response = "HTTP/1.1 %i\r\n" % code

    headers["server"] = "esp32server"
    headers["connection"] = "close"
    for k, v in headers.items():
        response += "%s: %s\r\n" % (k, v)

    response += data
    response += "\r\n"

    client.send(response.encode("utf-8"))
    client.close()

def on_request(rule, request_handler):
    regex = "^"
    rule_parts = rule.split("/")
    for part in rule_parts:
        var = variable_re.match(part)
        if var:
            regex += r"([a-zA-Z0-9_-]+)\/"
        else:
            regex += part + r"\/"
    regex += "?$"
    routes.append(
        (re.compile(regex), {"func": request_handler})
    )

def route(rule):
    return lambda func: on_request(rule, func)

def match_route(path):
    for matcher, route in routes:
        match = matcher.match(path)
        if match:
            return (match.groups(), route)
    return None

@route("/led_on")
def led_on(request):
    print("led on!")
    pixels.fill((128, 64, 128))
    pixels.show()
    return ("200 OK", [], "led on!")

pixels.fill((16, 64, 128))
pixels.show()
print("Pixels enabled.")

while True:
    client, remote_address = socket.accept()
    print("Received request from:", remote_address)
    request = get_request(client)
    if request:
        (method, path, params, headers, data) = request
        print(path)
        match = match_route(path)
        if match:
            args, route = match
            status, headers, resp_data = route["func"](request, *args)

    headers = {"content-type": "application/json"}
    body = '{success: true}'
    send_response(client, 200, headers, body)
