import math
from bullet import Bullet


class Player:
    def __init__(self, player_id, color, pos, canon):
        self.player_id = player_id
        self.color = color
        self.pos = pos
        self.canon = canon

        # INFO
        self.radius = 25
        self.speed = 5
        self.angle = 0
        self.canon_speed = 0.1
        self.ammo = 5

    def move(self, inputs):
        x, y = 0, 0
        px, py = self.pos

        if inputs['right']:
            x += self.speed
        if inputs['left']:
            x -= self.speed
        if inputs['down']:
            y += self.speed
        if inputs['up']:
            y -= self.speed

        if 75 < px + x < 525:
            px += x
        if 75 < py + y < 725 and not (175 < py + y < 625):
            py += y

        self.pos = (px, py)

    def rotate_canon(self, inputs):
        if inputs['rr']:
            if self.color == (255, 0, 0):
                self.angle += 0.1
            else:
                self.angle -= 0.1
        if inputs['rl']:
            if self.color == (255, 0, 0):
                self.angle -= 0.1
            else:
                self.angle += 0.1

        x = int(math.cos(self.angle) * self.radius) + self.pos[0]
        y = int(math.sin(self.angle) * self.radius) + self.pos[1]
        self.canon = (x, y)

    def shoot(self, inputs):
        if inputs['shoot'] and self.ammo:
            ax = math.cos(self.angle)
            bx = math.sin(self.angle)
            x = int(2 * ax * self.radius) + self.pos[0]
            y = int(2 * bx * self.radius) + self.pos[1]
            self.ammo -= 1
            return Bullet((x, y), self.color, (ax, bx))
        return None

    def update(self, inputs):
        self.move(inputs)
        self.rotate_canon(inputs)
        return self.shoot(inputs)


class SketchPlayer(Player):
    def __init__(self, mapping):
        super().__init__(*(mapping[attributes] for attributes in mapping))

    def draw(self, pg, wn):
        pg.draw.circle(wn, self.color, self.pos, self.radius)
        pg.draw.line(wn, (255, 255, 255), self.pos, self.canon, 5)
