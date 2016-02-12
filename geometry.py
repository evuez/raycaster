from math import cos
from math import sin
from pyglet.gl import glColor4f
from pyglet.gl import glBegin
from pyglet.gl import glEnd
from pyglet.gl import glLineWidth
from pyglet.gl import glVertex2f
from pyglet.gl import GL_POLYGON
from pyglet.gl import GL_LINES


def rectangle(x1, y1, x2, y2, color=(1, 0, 0, 1)):
    glColor4f(*color)
    glBegin(GL_POLYGON)
    glVertex2f(x1, y1)
    glVertex2f(x1, y2)
    glVertex2f(x2, y2)
    glVertex2f(x2, y1)
    glEnd()


def square(x, y, size, color=(1, 0, 0, 1)):
    x1, x2 = x, x + size
    y1, y2 = y, y + size
    rectangle(x1, y1, x2, y2, color)


def line(x, y, size, angle, color=(1, 0, 0, 1), thickness=1):
    x1, y1 = x, y
    x2, y2 = x1 + cos(angle) * size, y1 + sin(angle) * size
    glColor4f(*color)
    glLineWidth(thickness)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()
