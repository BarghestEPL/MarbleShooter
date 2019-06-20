import time
import math
import random
from player import Player

BLUE = BLUE_COLOR, BLUE_POS, BLUE_CANON = (0, 0, 255), (500, 700), (500, 675)
RED = RED_COLOR, RED_POS, RED_CANON = (255, 0, 0), (100, 100), (100, 125)


class PhysicEngine:
    def __init__(self):
        self.connected = []
        self.state = {'player': [],
                      'bullet': []}

        # INFO
        self.playing = False

    @staticmethod
    def distance(a, b):
        ax, ay = a
        bx, by = b
        x = math.pow(ax - bx, 2)
        y = math.pow(ay - by, 2)
        return math.sqrt(x + y)

    def get_state(self):
        mapping = {}
        for key in self.state:
            mapping[key] = []
            for item in self.state[key]:
                mapping[key].append(vars(item))
        return mapping

    def start(self):
        if len(self.connected) >= 2:
            player1 = random.randint(0, len(self.connected) - 1)
            player2 = player1
            while player2 == player1:
                player2 = random.randint(0, len(self.connected) - 1)

            blue = Player(self.connected[player1], *BLUE)
            red = Player(self.connected[player2], *RED)
            self.state['player'] = [blue, red]
            self.state['bullet'] = []
            self.playing = True
        else:
            self.playing = False

    def lose(self, player):
        for bullet in self.state['bullet']:
            if self.distance(player.pos, bullet.pos) < player.radius + bullet.radius:
                if bullet.color == player.color:
                    self.state['bullet'].remove(bullet)
                    player.ammo += 1
                else:
                    return True
        return False

    def move_bullet(self):
        for bullet in self.state['bullet']:
            x, y = bullet.pos
            dx, dy = bullet.direction
            if not (65 < x < 540):
                dx = -dx
            if not (65 < y < 740):
                dy = -dy
            bullet.direction = (dx, dy)
            bullet.pos = (x + int(bullet.speed * dx), y + int(bullet.speed * dy))

    def is_playing(self, pid):
        for player in self.state['player']:
            if player.player_id == pid:
                return player
        return

    def connect_player(self, player_id):
        self.connected.append(player_id)

    def disconnect_player(self, player_id):
        self.connected.remove(player_id)
        if self.is_playing(player_id):
            self.start()

    def update(self, player_id, inputs):
        if self.playing:
            player = self.is_playing(player_id)
            if player:
                bullet = player.update(inputs)
                if bullet:
                    self.state['bullet'].append(bullet)
                self.move_bullet()
                if self.lose(player):
                    self.start()
        else:
            self.start()
