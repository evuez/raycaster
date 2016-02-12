from pyglet import app
from pyglet.clock import schedule_interval
from pyglet.gl import glEnable
from pyglet.gl import glBlendFunc
from pyglet.gl import GL_BLEND
from pyglet.gl import GL_ONE_MINUS_SRC_ALPHA
from pyglet.gl import GL_SRC_ALPHA
from pyglet.window import key
from pyglet.window import Window
from geometry import rectangle
from raycaster import Map
from raycaster import Player


MAP_SIZE = 10

window = Window(MAP_SIZE * Map.SCALE, MAP_SIZE * Map.SCALE)

grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

map_ = Map.load(grid)
player = Player(map_, 4, 1)


def update(dt):
    player.move()
schedule_interval(update, 1 / 60)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.UP:
        player.actuator[0] = 1
    elif symbol == key.DOWN:
        player.actuator[0] = -1
    if symbol == key.LEFT:
        player.actuator[1] = -1
    elif symbol == key.RIGHT:
        player.actuator[1] = 1


@window.event
def on_key_release(symbol, modifiers):
    if symbol in (key.UP, key.DOWN):
        player.actuator[0] = 0
    if symbol in (key.LEFT, key.RIGHT):
        player.actuator[1] = 0


@window.event
def on_draw():
    window.clear()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    rectangle(0, 0, 500, 250, (0.58, 0.64, 0.65, 1))
    rectangle(0, 250, 500, 500, (0.17, 0.24, 0.31, 1))
    player.draw()


if __name__ == '__main__':
    app.run()


