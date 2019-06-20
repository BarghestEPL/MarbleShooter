import time
import socket
import threading
import helper_socket
from physic_engine import PhysicEngine


HP = HOST, PORT = '', 15987
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(HP)
socket.listen(5)

physic_engine = PhysicEngine()
connections = []


def run():
    while True:
        data = helper_socket.send_until(physic_engine.get_state())
        for client_socket in connections:
            try:
                client_socket.sendall(data)
            except ConnectionRefusedError:
                continue
            time.sleep(1/60)


def handler(client_socket, pid):
    while True:
        inputs = helper_socket.recv_until(client_socket)
        if inputs is None:
            connections.remove(client_socket)
            physic_engine.disconnect_player(pid)
            break
        physic_engine.update(pid, inputs)


def lobby():
    pid = 0
    while True:
        client_socket, _ = socket.accept()
        connections.append(client_socket)

        physic_engine.connect_player(pid)
        info = client_socket, pid

        client_thread = threading.Thread(target=handler, args=info, daemon=True)
        client_thread.start()
        pid += 1


lobby_thread = threading.Thread(target=lobby, daemon=True)
lobby_thread.start()
run()
