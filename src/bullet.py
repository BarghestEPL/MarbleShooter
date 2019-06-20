class Bullet:
    def __init__(self, pos, color, direction):
        self.pos = pos
        self.color = color
        self.direction = direction
        self.radius = 10
        self.speed = 5


class SketchBullet(Bullet):
    def __init__(self, mapping):
        super().__init__(*(mapping[attributes] for attributes in mapping))

    def draw(self, pg, wn):
        pg.draw.circle(wn, self.color, self.pos, self.radius)
