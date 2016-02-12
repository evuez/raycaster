import geometry
from math import floor
from math import cos
from math import sin
from math import pi


TAU = 2 * pi


def darken(color, scale=1.0):
    return list(map(
        lambda x: min(max(x / scale, 0), x),
        color[:3]
    )) + list(color[3:])


class Map(object):
    SCALE = 50
    EMPTY = 0
    WALL = 1

    def __init__(self, size):
        self.size = size
        self.grid = None

    @classmethod
    def load(cls, grid):
        map_ = cls(len(grid))
        map_.grid = grid
        return map_

    def draw(self):
        for y, row in enumerate(self.grid):
            for x, val in enumerate(row):
                if val == self.EMPTY:
                    continue
                geometry.square(x * self.SCALE, y * self.SCALE, self.SCALE)

    def around(self, x, y, size):
        top, bottom = floor(y + size), floor(y)
        left, right = floor(x), floor(x + size)
        tl = self.grid[top][left]
        tr = self.grid[top][right]
        bl = self.grid[bottom][left]
        br = self.grid[bottom][right]
        if any(c == Map.WALL for c in (tl, tr, bl, br)):
            return Map.WALL
        return Map.EMPTY

    def inspect(self, x, y):
        x, y = floor(x), floor(y)
        return self.grid[y][x]


class Player(object):
    SIZE = 0.5
    SPEED = 0.04
    FOV = TAU / 4.5
    VRES = 100

    def __init__(self, map_, x, y):
        self.map = map_
        self.size = self.map.SCALE * self.SIZE
        self.actuator = [0, 0]  # (forward / backward, left / right)
        self.pose = Pose(x, y, pi)
        self.size = self.SIZE * self.map.SCALE
        self.column_thickness = self.map.size * self.map.SCALE / self.VRES

    def draw(self):
        self.cast_rays()

    def move(self):
        speed = self.SPEED * self.actuator[0]
        next_x = self.pose.x + cos(self.pose.direction) * speed
        next_y = self.pose.y + sin(self.pose.direction) * speed
        if self.map.around(next_x, next_y, self.SIZE) == Map.EMPTY:
            self.pose.x, self.pose.y = next_x, next_y
        self.pose.direction += self.SPEED * self.actuator[1]

    def cast_rays(self):
        angle_increment = self.FOV / self.VRES
        angle = self.pose.direction - self.FOV / 2
        for c in range(self.VRES):
            self.cast_ray(c, angle)
            angle += angle_increment

    def cast_ray(self, column, angle):
        maxlen = length = self.map.size * self.map.SCALE
        x, y = cos(angle), sin(angle)
        for l in range(length):
            _x = self.pose.x + self.SIZE / 2 + x * l / self.map.SCALE
            _y = self.pose.y + self.SIZE / 2 + y * l / self.map.SCALE
            if self.map.inspect(_x, _y) == Map.WALL:
                length = l
                break
        geometry.line(
            column * self.column_thickness,
            self.map.size * self.map.SCALE / 2 - 6000 / length / 2,
            6000 / length,
            pi / 2,
            darken((0.75, 0.22, 0.16, 1), length * 8 / maxlen),
            self.column_thickness
        )


class Pose(object):

    def __init__(self, x, y, direction):
        self.x, self.y = x, y
        self._direction = direction

    def __str__(self):
        return 'Pose(x={}, y={}, direction={})'.format(
            self.x,
            self.y,
            self.direction
        )

    @property
    def direction(self):
        return self._direction
    @direction.setter
    def direction(self, value):
        self._direction = value
        self._direction %= TAU

