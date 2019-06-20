import inspect
from player import SketchPlayer
from bullet import SketchBullet

BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (222, 222, 222)
BLACK = (0, 0, 0)


class GraphicEngine:
    def __init__(self, pg, wn):
        self.pg = pg
        self.wn = wn

        self.__drawings = []
        self.__sketch = {'player': SketchPlayer,
                         'bullet': SketchBullet}

    @staticmethod
    def mapper(item, sketch):
        mapped = {}
        for param in inspect.signature(sketch.mro()[1]).parameters:
            mapped[param] = item[param]
        return mapped

    def __background(self):
        self.wn.fill(GREY, (0, 0, 600, 800))
        self.wn.fill(BLACK, (50, 50, 500, 700))
        self.pg.draw.line(self.wn, WHITE, (50, 600), (550, 600))
        self.pg.draw.line(self.wn, WHITE, (50, 200), (550, 200))

    def update(self, data):
        drawings = []
        for key in data:
            for item in data[key]:
                to_build = self.__sketch[key]
                mapped = self.mapper(item, to_build)
                drawings.append(to_build(mapped))
        self.__drawings = drawings

    def draw(self):
        self.__background()
        for item in self.__drawings:
            item.draw(self.pg, self.wn)
