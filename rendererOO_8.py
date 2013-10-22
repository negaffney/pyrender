##This version adds slightly buggy polygon support.
##It initializes with stable points rather than polygons,
##with the polygon initializers commented out for easy access.

from __future__ import division
from matrices_4 import matrix
import math, Tkinter, msvcrt, random

canvwidth = 500
canvheight = 500
master_tkinter = Tkinter.Tk()
canvas = Tkinter.Canvas(master_tkinter, width=canvwidth, height=canvheight)
canvas.pack()

class Camera:
    def __init__(self, loc = [0, 0, 0]):
        losvector = matrix(4, 1)
        losvector.set_entire_matrix([[loc[0]], [loc[1]], [loc[2] + 1], [1]])
        locvector = matrix(4, 1)
        locvector.set_entire_matrix([[loc[0]], [loc[1]], [loc[2]], [1]])
        self.rotation_matrix = self.init_rotation_matrix(losvector, locvector)
        self.translation_matrix = self.init_translation_matrix(loc[0], loc[1], loc[2])
        self.transform_matrix = self.rotation_matrix.multiply(self.translation_matrix)

    def distance_to(self, other, fast=False):
        a = ((other.get_cell(0, 0) - self.translation_matrix.get_cell(0, 3))**2 +
             (other.get_cell(1, 0) - self.translation_matrix.get_cell(1, 3))**2 +
             (other.get_cell(2, 0) - self.translation_matrix.get_cell(2, 3))**2)
        if fast:
            return a
        else:
            return math.sqrt(a)

    ##Several of these methods should be static in the java version
    def init_rotation_matrix(self, los, location):
    ##vectors x, y, and z will be their respective axes on a normalized coordinate system with the character at (0, 0, 0) looking directly down the z axis,
        ##z is calculated first as it is used in the calculation of the others
        los = los.subtract(location)
        los.set_cell(3, 0, 1)
        z = los.normalize()
        #world y axis unit vector
        yw = matrix(4, 1)
        yw.set_cell(1, 0, 1)
        y = yw.subtract(z.multiply(yw.dot(z)))
        x = z.cross(y)

        ##the vectors each become their own row in the final matrix
        rot_matrix = matrix(4, 4)
        rot_matrix.set_entire_matrix([[x.get_cell(0, 0), x.get_cell(1, 0), x.get_cell(2, 0), 0],
                                      [y.get_cell(0, 0), y.get_cell(1, 0), y.get_cell(2, 0), 0],
                                      [z.get_cell(0, 0), z.get_cell(1, 0), z.get_cell(2, 0), 0],
                                      [0, 0, 0, 1]])
        return rot_matrix

    ##static
    def init_translation_matrix(self, x, y, z):
        trans_matrix = matrix(4, 4)
        trans_matrix.set_entire_matrix([[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]])
        return trans_matrix

    def rotate_vertical(self, angle):
        angle = -angle
        cos = math.cos(angle)
        sin = math.sin(angle)
        temp_rot_matrix = matrix(4, 4)
        temp_rot_matrix.set_entire_matrix([[1, 0, 0, 0],
                                           [0, cos, -sin, 0],
                                           [0, sin, cos, 0],
                                           [0, 0, 0, 1]])
        self.rotation_matrix = temp_rot_matrix.multiply(self.rotation_matrix)
        self.update_transform_matrix()

    def bounded_rotate_vertical(self, angle, a = True):
##        angle = -angle
##        cos = math.cos(angle)
##        sin = math.sin(angle)
##        temp_rot_matrix = matrix(4, 4)
##        temp_rot_matrix.set_entire_matrix([[1, 0, 0, 0],
##                                           [0, cos, -sin, 0],
##                                           [0, sin, cos, 0],
##                                           [0, 0, 0, 1]])
##        temp_rot_2 = temp_rot_matrix.multiply(self.rotation_matrix)
##        for i in [0, 1]:
##            for j in range(3):
##                self.rotation_matrix.set_cell(i, j, temp_rot_2.get_cell(i, j))
##        self.update_transform_matrix()
        self.rotate_vertical(angle)

    def rotate_horizontal(self, angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        temp_rot_matrix = matrix(4, 4)
        temp_rot_matrix.set_entire_matrix([[cos, 0, sin, 0],
                                           [0, 1, 0, 0],
                                           [-sin, 0, cos, 0],
                                           [0, 0, 0, 1]])
        self.rotation_matrix = temp_rot_matrix.multiply(self.rotation_matrix)
        self.update_transform_matrix()

    def bounded_rotate_horizontal(self, angle):
##        cos = math.cos(angle)
##        sin = math.sin(angle)
##        temp_rot_matrix = matrix(4, 4)
##        temp_rot_matrix.set_entire_matrix([[cos, 0, sin, 0],
##                                           [0, 1, 0, 0],
##                                           [-sin, 0, cos, 0],
##                                           [0, 0, 0, 1]])
##        temp_rot_2 = temp_rot_matrix.multiply(self.rotation_matrix)
##        up = matrix(4, 1)
##        up.set_cell(1, 0, 1)
##        up = self.rotation_matrix.multiply(up)
##        for i in [0, 2]:
##            for j in range(3):
##                self.rotation_matrix.set_cell(i, j, temp_rot_2.get_cell(i, j))
##        for i in range(3):
##            self.rotation_matrix.set_cell(1, i, up.get_cell(i, 0))
##        self.update_transform_matrix()
##        self.bounded_rotate_vertical(self.vertical_rotation, False)
        self.rotate_horizontal(angle)
        
    def roll(self, angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        temp_rot_matrix = matrix(4, 4)
        temp_rot_matrix.set_entire_matrix([[cos, -sin, 0, 0],
                                           [sin, cos, 0, 0],
                                           [0, 0, 1, 0],
                                           [0, 0, 0, 1]])
        self.rotation_matrix = temp_rot_matrix.multiply(self.rotation_matrix)
        self.update_transform_matrix()

    def move_left(self, distance):
        ##first row of transform matrix multiplied by the distance and added to corrsponding elements of the 4th column
        for i in range(3):
            self.translation_matrix.set_cell(i, 3, self.translation_matrix.get_cell(i, 3) + distance * self.transform_matrix.get_cell(0, i))
        self.update_transform_matrix()

    def bounded_move_left(self, distance):
        self.translation_matrix.set_cell(0, 3, self.translation_matrix.get_cell(0, 3) + distance * self.transform_matrix.get_cell(0, 0))
        self.translation_matrix.set_cell(2, 3, self.translation_matrix.get_cell(2, 3) + distance * self.transform_matrix.get_cell(0, 2))
        self.update_transform_matrix()

    def move_up(self, distance):
        ##second row of transform matrix multiplied by the distance and added to corrsponding elements of the 4th column
        for i in range(3):
            self.translation_matrix.set_cell(i, 3, self.translation_matrix.get_cell(i, 3) + distance * self.transform_matrix.get_cell(1, i))
        self.update_transform_matrix()

    def bounded_move_up(self, distance):
        self.translation_matrix.set_cell(1, 3, self.translation_matrix.get_cell(1, 3) + distance * self.transform_matrix.get_cell(1, 1))
        self.update_transform_matrix()
        
    def move_forward(self, distance):
        ##third row of transform matrix multiplied by the distance and added to corrsponding elements of the 4th column
        for i in range(3):
            self.translation_matrix.set_cell(i, 3, self.translation_matrix.get_cell(i, 3) - distance * self.transform_matrix.get_cell(2, i))
        self.update_transform_matrix()

    def bounded_move_forward(self, distance):
        self.translation_matrix.set_cell(0, 3, self.translation_matrix.get_cell(0, 3) - distance * self.transform_matrix.get_cell(2, 0))
        self.translation_matrix.set_cell(2, 3, self.translation_matrix.get_cell(2, 3) - distance * self.transform_matrix.get_cell(2, 2))
        self.update_transform_matrix()
    
    def update_transform_matrix(self):
        ##the matrices need to be remultipled each time they change
        self.transform_matrix = self.rotation_matrix.multiply(self.translation_matrix)

    def distance(self, x1, y1, z1, x2, y2, z2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

    def get_2D_coordinates_and_distance(self, point):
        point = self.transform_matrix.multiply(point)
        x = point.get_cell(0, 0)
        y = point.get_cell(1, 0)
        z = point.get_cell(2, 0)
        dist = self.distance(0, x, 0, y, 0, z)
        if z <= 0:
            return None
        else:
            return x/z, y/z, dist

    def get_2D_coordinates(self, point):
        point = self.transform_matrix.multiply(point)
        x = point.get_cell(0, 0)
        y = point.get_cell(1, 0)
        z = point.get_cell(2, 0)
        if z <= 0:
            return None
        else:
            return x/z, y/z

    def get_polygon_point_coordinates(self, point):
        point = self.transform_matrix.multiply(point)
        x = point.get_cell(0, 0)
        y = point.get_cell(1, 0)
        z = point.get_cell(2, 0)
        if z == 0:
            z = -.0000000000001
        if z < 0:
            x = -x/z
            y = -y/z
            x *= canvwidth
            y *= canvheight
            x += (canvwidth/2)
            y += (canvheight/2)
            return x, y, False
        else:
            x = x/z
            y = y/z
            x *= canvwidth
            y *= canvheight
            x += (canvwidth/2)
            y += (canvheight/2)
            return x, y, True

##this is going to change when we have boids instead of points
class World:
    def __init__(self, camera):
        self.camera = camera
        self.points = []
        self.polygons = []

    def add_point(self, x, y, z):
        point = matrix(4, 1)
        point.set_entire_matrix([[x], [y], [z], [1]])
        self.points.append(point)

    def add_polygon(self, polygon):
        self.polygons.append(polygon)

    def convert_2D_coords(self, x, y):
        x *= canvwidth
        y *= canvheight
        x += (canvwidth/2)
        y += (canvheight/2)
        return x, y

    def draw_point(self, x, y):
        x *= canvwidth
        y *= canvheight
        x += (canvwidth/2)
        y += (canvheight/2)
        canvas.create_line(x, y, x, y+1)

    def draw_circle(self, x, y, size, color = 'blue'):
        x *= canvwidth
        y *= canvheight
        x += (canvwidth/2)
        y += (canvheight/2)
        canvas.create_oval(x-size/2, y-size/2, x+size/2, y+size/2, fill=color)

    def draw_all_points(self, circles = True):
        self.points.sort(key=lambda point:self.camera.distance_to(point), reverse=False)
        canvas.delete('all')
        if circles:
            map(lambda i: self.draw_circle(i[0], i[1], 500 / (i[2] + .0001), color=random.choice(['red', 'blue', 'green', 'yellow'])), filter(None, map(self.camera.get_2D_coordinates_and_distance, self.points)))
        else:
            map(self.draw_point, filter(None, map(self.camera.get_2D_coordinates, self.points)))
        canvas.update()

    def bitcode(self, point):
        bitcode = 0
        x = point[0]
        y = point[1]
        z = point[2]
##        if x < 0:
##            bitcode += 1
##        elif x > canvwidth:
##            bitcode += 2
##        if y < 0:
##            bitcode += 4
##        elif y > canvheight:
##            bitcode += 8
##        if not z:
##            bitcode += 16
        bitcode += (x < 0) + 2 * (x > canvwidth) + 4 * (y < 0) + 8 * (y > canvheight) + (not z) * 16
        return bitcode

    def on_screen(self, points):
        l = len(points)
        off = True
        for i in range(l):
            b1 = self.bitcode(points[i])
            j = (i+1)%l
            b2 = self.bitcode(points[j])
            if not (b1 & b2):
                off = False
        return not off
    
    def draw_all_polygons(self):
        canvas.delete('all')
        for polygon in self.polygons:
            converted = []
            points  = map(self.camera.get_polygon_point_coordinates, polygon.points)
            on = self.on_screen(points)
            converted = []
            for i in points:
                converted += [i[0], i[1]]
            if on:
                canvas.create_polygon(converted, fill=polygon.color)
        canvas.update()

class Polygon:

    def __init__(self, color):
        self.points = []
        self.color = color

    def add_point(self, x, y, z):
        point = matrix(4, 1)
        point.set_entire_matrix([[x], [y], [z], [1]])
        self.points.append(point)

    def get_points():
        return self.points

w = World(Camera([0, 0, 100]))
for i in range(-20, 20, 5):
    for j in range(-20, 20, 5):
        w.add_point(i, j, 20)
        w.add_point(20, i, j)
        w.add_point(-20, i, j)
        w.add_point(i, j, -20)
        w.add_point(i, -20, j)
        w.add_point(i, 20, j)

##p = Polygon('red')
##p.add_point(-5, 0, 20)
##p.add_point(5, 0, 20)
##p.add_point(5, 5, 20)
##w.add_polygon(p)
##
##p = Polygon('red')
##p.add_point(-5, 0, 20)
##p.add_point(-5, 5, 20)
##p.add_point(5, 5, 20)
##w.add_polygon(p)
##
##p = Polygon('blue')
##p.add_point(-5, 0, 20)
##p.add_point(-5, 5, 20)
##p.add_point(-5, 5, 15)
##w.add_polygon(p)
##
##p = Polygon('blue')
##p.add_point(-5, 0, 20)
##p.add_point(-5, 0, 15)
##p.add_point(-5, 5, 15)
##w.add_polygon(p)
##
##p = Polygon('green')
##p.add_point(5, 0, 20)
##p.add_point(5, 5, 20)
##p.add_point(5, 5, 15)
##w.add_polygon(p)
##
##p = Polygon('green')
##p.add_point(5, 0, 20)
##p.add_point(5, 0, 15)
##p.add_point(5, 5, 15)
##w.add_polygon(p)



movement_rate = 2
rotation_rate = math.pi/100

user_input = None
bounded = False
while user_input != 'e':
    if user_input == 'q':
        bounded = eval('not bounded')
    elif user_input == 'w':
        eval('w.camera.' + 'bounded_'*bounded + 'move_forward(movement_rate)')
    elif user_input == 'a':
        eval('w.camera.' + 'bounded_'*bounded + 'move_left(movement_rate)')
    elif user_input == 's':
        eval('w.camera.' + 'bounded_'*bounded + 'move_forward(-movement_rate)')
    elif user_input == 'd':
        eval('w.camera.' + 'bounded_'*bounded + 'move_left(-movement_rate)')
    elif user_input == 'k':
        eval('w.camera.' + 'bounded_'*bounded + 'rotate_horizontal(rotation_rate)')
    elif user_input == ';':
        eval('w.camera.' + 'bounded_'*bounded + 'rotate_horizontal(-rotation_rate)')
    elif user_input == 'l':
        eval('w.camera.' + 'bounded_'*bounded + 'rotate_vertical(-rotation_rate)')
    elif user_input == 'o':
        eval('w.camera.' + 'bounded_'*bounded + 'rotate_vertical(rotation_rate)')
    elif user_input == 'r':
        eval('w.camera.' + 'bounded_'*bounded + 'move_up(movement_rate)')
    elif user_input == 'f':
        eval('w.camera.' + 'bounded_'*bounded + 'move_up(-movement_rate)')
    elif user_input == 'x':
        w.camera.roll(-rotation_rate)
    elif user_input == 'z':
        w.camera.roll(rotation_rate)

    w.draw_all_points()
    user_input = msvcrt.getch()

canvas.mainloop()



