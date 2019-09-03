from gravity import point, body
import sys


def setupSolarSystem():
    sun = {"loc": point(0., 0.), "mass": 1, "vel": point(0., 0.), "dispMass": 8, "colour": (255, 255, 0)}
    jupiter = {"loc": point(0., 5.203), "mass": 0.0009543, "vel": point(2.762, 0.), "dispMass": 7, "colour": (255, 0, 0)}
    mercury = {"loc": point(0, .39), "mass": 1.652e-7, "vel": point(9.992, 0), "dispMass": 2, "colour": (211, 211, 211)}
    venus = {"loc": point(0, 0.723), "mass": 0.000002447, "vel": point(7.378, 0), "dispMass": 3, "colour": (255, 255, 153)}
    earth = {"loc": point(0, 1), "mass": 0.000003003, "vel": point(6.282, 0), "dispMass": 4, "colour": (30, 144, 255)}
    saturn = {"loc": point(0, 9.358), "mass": 0.000287, "vel": point(1.897, 0), "dispMass": 5, "colour": (139, 69, 19)}
    uranus = {"loc": point(0, 18.716), "mass": 4.374e-5, "vel": point(1.441, 0), "dispMass": 4, "colour": (135, 206, 250)}
    mars = {"loc": point(0, 1.52341740516), "mass": 3.213e-7, "vel": point(5.059, 0), "dispMass": 3, "colour": (255, 0, 0)}

    bodies = [body(loc=sun["loc"], mass=sun["mass"], vel=sun["vel"], name="sun", dispMass=sun["dispMass"], colour=sun["colour"]),
              body(loc=mercury["loc"], mass=mercury["mass"], vel=mercury["vel"], name="mercury", dispMass=mercury["dispMass"], colour=mercury["colour"]),
              body(loc=venus["loc"], mass=venus["mass"], vel=venus["vel"], name="venus", dispMass=venus["dispMass"], colour=venus["colour"]),
              body(loc=earth["loc"], mass=earth["mass"], vel=earth["vel"], name="earth", dispMass=earth["dispMass"], colour=earth["colour"]),
              body(loc=jupiter["loc"], mass=jupiter["mass"], vel=jupiter["vel"], name="jupiter", dispMass=jupiter["dispMass"], colour=jupiter["colour"]),
              body(loc=saturn["loc"], mass=saturn["mass"], vel=saturn["vel"], name="saturn", dispMass=saturn["dispMass"], colour=saturn["colour"]),
              body(loc=mars["loc"], mass=mars["mass"], vel=mars["vel"], name="mars", dispMass=mars["dispMass"], colour=mars["colour"])]

    for i in range(0, 10):
        bodies = addTrojanBody(bodies, i)

    bodies = setComFrame(bodies)

    return bodies


def setComFrame(bodies):

    totMass = 0
    for body in bodies:
        totMass += body.mass
    rx = 0
    ry = 0
    vx = 0
    vy = 0
    for body in bodies:
        rx += (body.mass / totMass) * body.loc.x
        ry += (body.mass / totMass) * body.loc.y
        vx += (body.mass / totMass) * body.vel.x
        vy += (body.mass / totMass) * body.vel.y

    for body in bodies:
        body.loc.x -= rx
        body.loc.y -= ry
        body.vel.x -= vx
        body.vel.y -= vy

    return bodies


def debugPrintOut(children, quad):
    if quad:
        for n in children:
            pg.draw.rect(screen, (255, 255, 255), [hWidth + int(n.x0 * mag), hHeight + int(n.y0 * mag), n.width * mag, n.height * mag], 1)

    fps = font.render("FPS:" + str(int(clock.get_fps())), True, pg.Color('white'))
    screen.blit(fps, (10, 10))

    Ocount = font.render("Bodies:" + str(count), True, pg.Color('white'))
    screen.blit(Ocount, (10, 30))

    masstxt = font.render("Total Mass:" + str(massTot), True, pg.Color('white'))
    screen.blit(masstxt, (10, 50))

    stepsTxt = font.render("Steps done:" + str(steps), True, pg.Color('white'))
    screen.blit(stepsTxt, (10, 70))


def removeBodyOutofBounds(bodies, count):
    massTot = 0.
    for cbody in bodies:
        massTot += cbody.mass
        if (cbody.loc.x * mag + 960) > 1920 or (cbody.loc.x * mag + 960) < 0:
            bodies.remove(cbody)
            count -= 1
        elif (cbody.loc.y * mag + 540) > 1080 or (cbody.loc.y * mag + 540) < 0:
            bodies.remove(cbody)
            count -= 1
    return bodies, massTot


def writeOut(paths):
    for path in paths:
        file = open(path["name"] + ".dat", "w")
        for i, j in zip(path["x"], path["y"]):
            file.write(str(i) + " " + str(j) + " " + "\n")
        file.close()


if __name__ == '__main__':

    import pygame as pg
    from gravity import euler_integrator, addTrojanBody, runSim
    import numpy as np

    WIDTH = 1920
    HEIGHT = 1080
    hWidth = int(WIDTH / 2)
    hHeight = int(HEIGHT / 2)

    dt = 1./(10.*365.)
    debug = False
    drawQaud = False
    steps = 0
    trail = False
    mag = 50

    pg.init()
    font = pg.font.Font(None, 30)
    clock = pg.time.Clock()
    size = WIDTH, HEIGHT
    screen = pg.display.set_mode(size, pg.RESIZABLE)
    pg.display.set_caption("N-body simulator")

    bodies = setupSolarSystem()

    systemHist = []
    for tmpBody in bodies:
        systemHist.append({"x": [], "y": [], "z": [], "name": tmpBody.name})

    integrator = euler_integrator(timestep=dt, bodies=bodies, screen=screen, size=[WIDTH, HEIGHT, hWidth, hHeight], mag=mag)
    count = len(bodies)

    while True:
        screen.fill((0, 0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                writeOut(systemHist)
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                    debug = not debug
                elif event.key == pg.K_t:
                    trail = not trail
                elif event.key == pg.K_q:
                    drawQaud = not drawQaud
                elif event.key == pg.K_p:
                    mag += 1
                    integrator.mag = mag
                    mag = max(0, mag)
                elif event.key == pg.K_o:
                    mag -= 1
                    integrator.mag = mag
                    mag = max(0, mag)
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    bodies = addTrojanBody(bodies, count)
                    count += 1
                    systemHist.append({"x": [], "y": [], "z": [], "name": f"added{count}"})
                    integrator.bodies = bodies
                elif event.button == 4:
                    mag -= 1
                    mag = max(0, mag)
                    integrator.mag = mag
                elif event.button == 5:
                    mag += 1
                    mag = max(0, mag)
                    integrator.mag = mag

            if event.type == pg.VIDEORESIZE:
                oldSurface = screen
                WIDTH = event.w
                hWidth = int(WIDTH / 2)
                HEIGHT = event.h
                hHeight = int(HEIGHT / 2)
                screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                integrator.screen = screen
                integrator.size = [WIDTH, HEIGHT, hWidth, hHeight]
                del oldSurface

        systemHist, children = runSim(integrator, steps, bodies, systemHist)
        if trail:
            for i in systemHist:
                xtmp = np.array(i["x"][-100:])*mag + hWidth
                ytmp = np.array(i["y"][-100:])*mag + hHeight
                xtmp = xtmp.astype(int)
                ytmp = ytmp.astype(int)
                pts = list(zip(xtmp, ytmp))

                if len(pts) > 1:
                    pg.draw.lines(screen, (255, 255, 255), False, pts, 1)

        clock.tick()
        bodies, massTot = removeBodyOutofBounds(bodies, count)
        if debug:
            debugPrintOut(children, drawQaud)

        pg.display.flip()
        steps += 1
