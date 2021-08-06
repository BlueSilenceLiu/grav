#!/usr/bin/env python3
"""
basic code from: turtledemo.planet_and_moon

* must add a mainloop() in the lastline of your code! or there will be an error from Threading!
  (haven't found the solution)
  but you can use GravSys.run() instead of GravSys.start() to avoid this, the disadvantage is that you must wait before
  emulating end, and without mainloop(), the window will close after graphing.
  FIXME: find the solution

  thanks for these programmer who help me test and debug:
      -
  author:
      Blue S. Liu

"""
from turtle import Shape, Turtle, bgcolor, bgpic, mainloop, Screen, Vec2D as Vec
from threading import *

G = 8
PLANET = "planet"
STAR = "circle"

_have_setup = False


class _GravSysThread(Thread):
    def __init__(self, gravSys):
        super().__init__()
        self.gravSys = gravSys

    def run(self):
        self.gravSys.run()


class GravSys(object):
    syss = []

    def __init__(self, dt=0.01, turn=1000):
        """
        turn must be a int that greater than 0. if it is 0, it can never stop!
        """
        if _have_setup:
            self.__class__.syss.append(self)
            self.planets = []
            self.t = 0
            self.dt = dt
            self.turn = turn
        else:
            raise Exception("basic information haven't setup.")

    def _init(self):
        for p in self.planets:
            p.init()

    def run(self):
        self._init()
        for i in range(self.turn):
            self.t += self.dt
            for p in self.planets:
                p.step()

    def start(self):
        """
        This function can use a new Threading so that you can emulate more than one at the same time.
        """
        emulation = _GravSysThread(self)
        emulation.start()


class Star(Turtle):
    def __init__(self, m, x: Vec, v: Vec, **kwargs: dict):
        """
        kwargs:
            gravSys: a GravSys object, the gravity system that ths star exist;
                     If the attribute not exist, then:
                        1: if there have been a gravSys built, use the last one that created;
                        2: if there haven't been any gravSys, create one automatically.

            shape: the shape of star;
                    we recommend you to use PLANET(equals to 'planet') as a planet that can be delight,
                                         or STAR(equals to 'circle') as a sun that make light.
                    otherwise, it would be harder for user to watch(unless you have a specific use).

            pc: pencolor, effective when pd is True.
            pd: is pendown, a boolean.
                default value: True
        """
        try:
            Turtle.__init__(self, shape=kwargs["shape"])
        except KeyError:
            Turtle.__init__(self, shape=PLANET)
        self.penup()
        self.m = m
        self.setpos(x)
        self.v = v
        try:
            self.gravSys = kwargs["gravSys"]
            if self.gravSys.__class__ != GravSys:
                raise TypeError("gravSys must be a GravSys type")
        except KeyError:
            if not GravSys.syss:
                self.gravSys = GravSys()
            else:
                self.gravSys = GravSys.syss[-1]
        try:
            pd = kwargs['pd']
        except KeyError:
            pd = True
        if pd:
            self.pd()
        try:
            pc = kwargs['pc']
        except KeyError:
            pc = '#FFFFFF'
        self.color(pc, pc)
        self.gravSys.planets.append(self)
        self.resizemode("user")
        self.pendown()

    def init(self):
        dt = self.gravSys.dt
        self.a = self.acc()
        self.v = self.v + 0.5 * dt * self.a

    def acc(self):
        a = Vec(0, 0)
        for planet in self.gravSys.planets:
            if planet != self:
                v = planet.pos() - self.pos()
                a += (G * planet.m / abs(v) ** 3) * v
        return a

    def step(self):
        dt = self.gravSys.dt
        self.setpos(self.pos() + dt * self.v)
        if self.gravSys.planets.index(self) != 0:
            self.setheading(self.towards(self.gravSys.planets[0]))
        self.a = self.acc()
        self.v = self.v + dt * self.a


def setup(day_color="orange", night_color="black", background: tuple = ('c', "white")):
    """
    background: a tuple: (mode, value)
        mode has two available value: 'c' or 'f', if it isn't so, raise ValueError.
          when mode is 'c', value is the color ("#XXXXXX",
                                             or "black", "white", etc.,
                                             or a (r, g, b) tuple) of background;
          when mode is 'f', value is the path of background picture (only .gif file)
    """
    global _have_setup
    if _have_setup:
        raise Exception("Do not setup again!")
    _have_setup = True
    s = Turtle()
    s.reset()
    s.getscreen().tracer(0, 0)
    s.ht()
    s.pu()
    s.fd(6)
    s.lt(90)
    s.begin_poly()
    s.circle(6, 180)
    s.end_poly()
    m1 = s.get_poly()
    s.begin_poly()
    s.circle(6, 180)
    s.end_poly()
    m2 = s.get_poly()

    planetshape = Shape("compound")
    planetshape.addcomponent(m1, day_color)
    planetshape.addcomponent(m2, night_color)
    s.getscreen().register_shape("planet", planetshape)
    s.getscreen().tracer(1, 0)

    mode = background[0]
    value = background[1]
    if mode == 'c':
        if value.__class__ == tuple:
            bgcolor(value[0], value[1], value[2])
        elif value.__class__ == str:
            bgcolor(background[1])
        else:
            raise TypeError("unavailable type of background-value:"
                            + value.__class__.__name__)
    elif mode == 'f':
        bgpic(value)

def Window():
    return Screen()
