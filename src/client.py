import os
import socket
import threading
import pygame as pg
import helper_socket
from graphic_engine import GraphicEngine


os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()

pg.display.set_caption('MarbleShooter')
wn = pg.display.set_mode((600, 800))
graphic_engine = GraphicEngine(pg, wn)

clock = pg.time.Clock()
font = pg.font.SysFont('comicsansms', 36)
login_text = font.render('Waiting server response ...', True, (255, 255, 255))

run = True
access_deny = True
HP = HOST, PORT = '109.88.29.134', 15987
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send_inputs(shoot):
    keys = pg.key.get_pressed()
    inputs = {'shoot': shoot,
              'right': keys[pg.K_d],
              'left': keys[pg.K_a],
              'down': keys[pg.K_s],
              'up': keys[pg.K_w],
              'rr': keys[pg.K_KP4],
              'rl': keys[pg.K_KP6]}

    data = helper_socket.send_until(inputs)
    server_sock.sendall(data)


def rcv_state():
    while run:
        data = helper_socket.recv_until(server_sock)
        graphic_engine.update(data)


def run_game():
    global run
    server_state = threading.Thread(target=rcv_state, daemon=True)
    server_state.start()
    while run:
        clock.tick(60)
        shoot = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_KP5:
                    shoot = True

        send_inputs(shoot)
        graphic_engine.draw()
        pg.display.update()


def login_screen():
    global access_deny
    while access_deny:
        try:
            server_sock.connect(HP)
        except TimeoutError:
            continue
        access_deny = False


def login():
    global access_deny
    log_screen = threading.Thread(target=login_screen, daemon=True)
    log_screen.start()
    while access_deny:
        wn.blit(login_text, (100, 250))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                access_deny = False
        pg.display.update()
    run_game()
    pg.quit()


login()
