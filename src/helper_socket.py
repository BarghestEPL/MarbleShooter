import json


def recv_until(socket, until=b'\n'):
    data = b''
    while not data.endswith(until):
        try:
            data += socket.recv(1)
        except ConnectionResetError:
            return None
    data = data.replace(until, b'')
    return json.loads(data.decode('utf-8'))


def send_until(data, until=b'\n'):
    return json.dumps(data).encode('utf-8') + until
