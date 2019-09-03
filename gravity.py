import numpy as np
import pygame
from quadtree import qTree, findChild


class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class body:
    """loc in units of AU
        mass in solar mass units
        velociy in AU/yr
    """
    def __init__(self, loc, mass, vel, colour, dispMass, name=""):
        self.loc = loc
        self.mass = mass
        self.vel = vel
        self.name = name
        self.colour = colour
        self.dispMass = dispMass


class euler_integrator:

    def __init__(self, timestep, bodies, screen, size, mag):
        self.timestep = timestep
        self.bodies = bodies
        self.screen = screen
        self.size = size
        self.mag = mag

    def calcAccleration(self, bodyIdx):
        acc = point(0., 0.)
        targetBody = self.bodies[bodyIdx]
        for idx, body in enumerate(self.bodies):
            if idx != bodyIdx:
                mag = 1. / np.sqrt((targetBody.loc.x - body.loc.x)**2 +
                                   (targetBody.loc.y - body.loc.y)**2)**3
                acc.x += body.mass * ((body.loc.x - targetBody.loc.x) * mag)
                acc.y += body.mass * ((body.loc.y - targetBody.loc.y) * mag)
        return acc

    def calcVelocity(self):
        G = 4.*np.pi**2  # AU M (AU/yr)^2
        for idx, targetBody in enumerate(self.bodies):
            acc = self.calcAccleration(idx)
            targetBody.vel.x += G * self.timestep * acc.x
            targetBody.vel.y += G * self.timestep * acc.y

    def calcPosition(self):
        """
            updates postions and draws body on pygame screen
            also calculates quadtree for the collection of bodies
            returns list of children in quadtree for drawing
        """
        qt = qTree(1, self.size[1], self.size[0])
        for body in self.bodies:
            body.loc.x += body.vel.x * self.timestep
            body.loc.y += body.vel.y * self.timestep
            qt.addPoint(body.loc.x, body.loc.y, body.mass)
            pygame.draw.circle(self.screen, body.colour, (self.size[2] + int(body.loc.x * self.mag), self.size[3] + int(body.loc.y * self.mag)), body.dispMass)
        qt.subDivide()
        c = findChild(qt.root)
        del qt
        return c

    def doStep(self):
        self.calcVelocity()
        c = self.calcPosition()
        return c


def runSim(integrator, steps, bodies, Histo):

    c = integrator.doStep()
    if steps % 200 == 0:
        for idx, bodyLoc in enumerate(Histo):
            try:
                bodyLoc["x"].append(bodies[idx].loc.x)
                bodyLoc["y"].append(bodies[idx].loc.y)
            except IndexError:
                continue
    return Histo, c


def addTrojanBody(bodies, count):
    """
    adds a small body where the trojan bodies are
    """
    for tmpBody in bodies:
        if tmpBody.name == "jupiter":
            vel = point(0, 0)
            x1 = tmpBody.loc.x
            y1 = tmpBody.loc.y
            jupPhi = np.arctan2(y1, x1)
            jupPhi -= np.pi / 6.
            vel.x = tmpBody.vel.x * (np.random.rand() * .1 + .9)
            vel.y = tmpBody.vel.y * (np.random.rand() * .1 + .9)

    r = np.random.rand() * .2 + 5.1
    phi = np.random.rand() * 6 + (jupPhi * (180 / np.pi))
    phi *= (np.pi / 180.)
    pos = point(r * np.cos(phi), r * np.sin(phi))
    bodies.append(body(loc=pos, mass=1.652e-13, vel=vel, name=f"added{count}", dispMass=2, colour=(255, 255, 255)))

    return bodies
