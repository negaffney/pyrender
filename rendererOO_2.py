##This is the stable version, it initializes a tkinter window with a hollow cube made of points
##which can be navigated using W, A, S, and D for standard movement, R and F to move up and down,
##and K, O, L, ;, Z, and X for rotation.

from __future__ import division
from matrices_4 import matrix
import math, Tkinter, msvcrt

canvwidth = 500
canvheight = 500
master_tkinter = Tkinter.Tk()
canvas = Tkinter.Canvas(master_tkinter, width=canvwidth, height=canvheight)
canvas.pack()

class Camera:
    def __init__(self, loc = [0, 0, 0], los = [0, 0, 1]):
        losvector = matrix(4, 1)
        losvector.set_entire_matrix([[los[0]], [los[1]], [los[2]], [1]])
        locvector = matrix(4, 1)
        locvector.set_entire_matrix([[loc[0]], [loc[1]], [loc[2]], [1]])
        self.rotation_matrix = self.init_rotation_matrix(losvector, locvector)
        self.translation_matrix = self.init_translation_matrix(loc[0], loc[1], loc[2])
        self.transform_matrix = self.rotation_matrix.multiply(self.translation_matrix)

    ##Several of these methods should be static in the java version
    def init_rotation_matrix(self, los, location):
        '''initializes a rotation matrix using the method explained on http://www.fastgraph.com/makegames/3drotation/ given a starting line of sight'''
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
        '''initializes a translation matrix for movement, this is just an identity matrix with the last column changed to the location vector'''
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

    def move_up(self, distance):
        ##second row of transform matrix multiplied by the distance and added to corrsponding elements of the 4th column
        for i in range(3):
            self.translation_matrix.set_cell(i, 3, self.translation_matrix.get_cell(i, 3) + distance * self.transform_matrix.get_cell(1, i))
        self.update_transform_matrix()
        
    def move_forward(self, distance):
        ##third row of transform matrix multiplied by the distance and added to corrsponding elements of the 4th column
        for i in range(3):
            self.translation_matrix.set_cell(i, 3, self.translation_matrix.get_cell(i, 3) - distance * self.transform_matrix.get_cell(2, i))
        self.update_transform_matrix()
        
    def update_transform_matrix(self):
        ##the matrices need to be remultipled each time they change
        self.transform_matrix = self.rotation_matrix.multiply(self.translation_matrix)

    ##static
    def distance(self, x1, y1, z1, x2, y2, z2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

    def get_2D_coordinates_and_distance(self, point):
        point = self.transform_matrix.multiply(point)
        x = point.get_cell(0, 0)
        y = point.get_cell(1, 0)
        z = point.get_cell(2, 0)
        dist = self.distance(0, x, 0, y, 0, z)
        if z == 0:
            z = .00001
        elif z < 0:
            return None
        else:
            return x/z, y/z, dist

    def get_2D_coordinates(self, point):
        point = self.transform_matrix.multiply(point)
        x = point.get_cell(0, 0)
        y = point.get_cell(1, 0)
        z = point.get_cell(2, 0)
        if z == 0:
            z = .00001
        elif z < 0:
            return None
        else:
            return x/z, y/z

##this is going to change when we have boids instead of points
class World:
    def __init__(self, camera):
        self.camera = camera
        self.points = []

    def add_point(self, x, y, z):
        point = matrix(4, 1)
        point.set_entire_matrix([[x], [y], [z], [1]])
        self.points.append(point)

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
        canvas.create_oval(x-size/2, y-size/2, x+size/2, y+size/2, fill=color, outline=color)

    def draw_all_points(self, circles = True):
        canvas.delete('all')
        if circles:
            map(lambda i: self.draw_circle(i[0], i[1], 500 / (i[2] + .0001)), filter(None, map(self.camera.get_2D_coordinates_and_distance, self.points)))
        else:
            map(lambda i:self.draw_point(i[0], i[1]), filter(None, map(self.camera.get_2D_coordinates, self.points)))
        canvas.update()

w = World(Camera([0, 0, 0], [10, 10, 10]))
for i in range(-20, 21, 5):
    for j in range(-20, 21, 5):
        w.add_point(i, j, 20)
        w.add_point(20, i, j)
        w.add_point(-20, i, j)
        w.add_point(i, j, -20)
        w.add_point(i, -20, j)
        w.add_point(i, 20, j)

##for i in xrange(-60, 60):
##    i /= 3
##    for j in xrange(-60, 60):
##        j /= 3
##        w.add_point(i, j, 20)
##        w.add_point(20, i, j)
##        w.add_point(-20, i, j)
##        w.add_point(i, j, -20)
##        w.add_point(i, -20, j)
##        w.add_point(i, 20, j)

movement_rate = 2
rotation_rate = math.pi/100

user_input = None
while user_input != 'e':
    if user_input == 'w':
        w.camera.move_forward(movement_rate)
    elif user_input == 'a':
        w.camera.move_left(movement_rate)
    elif user_input == 's':
        w.camera.move_forward(-movement_rate)
    elif user_input == 'd':
        w.camera.move_left(-movement_rate)
    elif user_input == 'k':
        w.camera.rotate_horizontal(rotation_rate)
    elif user_input == ';':
        w.camera.rotate_horizontal(-rotation_rate)
    elif user_input == 'l':
        w.camera.rotate_vertical(-rotation_rate)
    elif user_input == 'o':
        w.camera.rotate_vertical(rotation_rate)
    elif user_input == 'r':
        w.camera.move_up(movement_rate)
    elif user_input == 'f':
        w.camera.move_up(-movement_rate)
    elif user_input == 'x':
        w.camera.roll(-rotation_rate)
    elif user_input == 'z':
        w.camera.roll(rotation_rate)

    w.draw_all_points()
    user_input = msvcrt.getch()

canvas.mainloop()



