import random
import sys

class Point():
    """docstring for Point"""
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

class Node():
    """docstring for Node"""
    def __init__(self, x0, y0, w, h, points):
        self.x0 = x0
        self.y0 = y0
        self.width = w
        self.height = h
        self.points = points
        self.com = None
        self.children = []

class qTree():
    """docstring for qTree"""
    def __init__(self, k, mx, my):
        super(qTree, self).__init__()
        self.threshold = k
        self.points = [] #[Point(random.uniform(0, 10), random.uniform(0, 10)) for x in range(n)]
        self.root = Node(-mx, -my, 2.*mx, 2.*my, self.points)


    def addPoint(self, x, y, mass):
        self.points.append(Point(x, y, mass))


    def subDivide(self):
        recursiveSubdivide(self.root, self.threshold)


    def graph(self):
        # fig, ax = plt.subplots()
        c = findChild(self.root)
        # for n in c:
            # ax.add_patch(patches.Rectangle((n.x0, n.y0), n.width, n.height, fill=False))
        x = [point.x for point in self.points]
        y = [point.y for point in self.points]
        # plt.scatter(x, y)
        # plt.show()
        return


    def getCom(self):
        return getComHelper(self.root)


def recursiveSubdivide(node, k):
    if len(node.points) <= k:
        return

    w_ = float(node.width / 2.)
    h_ = float(node.height / 2.)

    p = contains(node.x0, node.y0, w_, h_, node.points)
    x1 = Node(node.x0, node.y0, w_, h_, p)
    recursiveSubdivide(x1, k)

    p = contains(node.x0, node.y0 + h_, w_, h_, node.points)
    x2 = Node(node.x0, node.y0+h_, w_, h_, p)
    recursiveSubdivide(x2, k)

    p = contains(node.x0 + w_, node.y0, w_, h_, node.points)
    x3 = Node(node.x0 + w_, node.y0, w_, h_, p)
    recursiveSubdivide(x3, k)

    p = contains(node.x0 + w_, node.y0 + h_, w_, h_, node.points)
    x4 = Node(node.x0 + w_, node.y0 + h_, w_, h_, p)
    recursiveSubdivide(x4, k)

    node.children = [x1, x2, x3, x4]

def contains(x, y, w, h, points):
    pts = []
    for point in points:
        if point.x >= x and point.x <= x + w and point.y >= y and point.y <= y + h:
            pts.append(point)
    return pts


def getComHelper(node):
    if not node.children:
        if len(node.points) == 1:
            node.com = node.points[0]
            return node.com
        else:
            return Point(0, 0, 0)
    else:
        com = []
        for child in node.children:
            com.append(getComHelper(child))
    node.com = calcCom(com)
    return com


def calcCom(blah):
    x = 0
    y = 0
    mass = 0
    for i in blah:
        if type(i) != Point:
            tmp = calcCom(i)
            x += tmp.x
            y += tmp.y
            mass += tmp.mass
        else:
            x += i.x
            y += i.y
            mass += i.mass
    return Point(x / mass, y / mass, mass)

def findChild(node):
    if not node.children:
        return [node]
    else:
        children = []
        for child in node.children:
            children += (findChild(child))
    return children

if __name__ == '__main__':
    k = 1
    qt = qTree(k)

    qt.addPoint(2.5, 2.5, 2)

    qt.addPoint(2.5, 7.5, 2)

    qt.addPoint(6.25, 1.25, 2)
    qt.addPoint(8.75, 3.75, 2)

    qt.addPoint(5.625, 8.375, 2)
    qt.addPoint(6.775, 9.325, 2)
    qt.addPoint(6.975, 9.325, 2)
    qt.addPoint(6.75, 9.325, 2)

    qt.addPoint(8.75, 8.75, 2)


    qt.subDivide()
    qt.graph()
    objs = qt.getCom()
