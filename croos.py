import turtle as t
import math


s = 100
def draw_circle(radius):
    count = 360
    while count > 0:
        t.left(1)
        t.forward(math.pi * radius / 180)
        count -= 1

draw_circle(100)