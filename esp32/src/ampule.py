import io
import re

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
