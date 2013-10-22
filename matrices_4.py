
from __future__ import division
##Information:
##    The only methods of this class fit for human consumption are:
##        matrix (the initializer)
##        set_cell
##        get_cell
##        add
##        multiply
##        subtract
##        we may want to move these to a seperate vector class that uses 4x1 matricies
##            normalize
##            norm
##            cross
##            dot
##            distance
##    Those last three are smart enough to figure out if they're being passed a single number or an entire matrix.
##    Division is not implemented because it doesn't exist.
##    None of the mathematical methods are destructive; all of them simply return a value.

class matrix:
    import math

    #exceptions

    class IncompatibleMatrixException:
        def __str__(self):
            return 'The matrices have incompatible sizes.'
    
    def __init__(self, rows, columns):
        self.data = []
        for row in range(rows):
            toadd = []
            for column in range(columns):
                toadd.append(0)
            self.data.append(toadd)
        self.rows = rows
        self.columns = columns
        self.identitylist = []
##        for row in range(rows):
##            toadd = []
##            for column in range(rows):
##                if column == row: toadd.append(1)
##                else: toadd.append(0)
##            self.identitylist.append(toadd)

    #operations

    def set_cell(self, row, column, value):
        if (row >= self.rows) or (column >= self.columns) or (row < 0) or (column < 0):
            raise IndexError
        else:
            self.data[row][column] = value

    def get_cell(self, row, column):
        if (row >= self.rows) or (column >= self.columns) or (row < 0) or (column < 0):
            raise IndexError
        else:
            return self.data[row][column]

    def set_entire_matrix(self, list_of_lists):
        if (len(list_of_lists) != self.rows) or (len(list_of_lists[0]) != self.columns):
            raise self.IncompatibleMatrixException
        else:
            for row_number in range(len(list_of_lists)):
                for column_number in range(len(list_of_lists[row_number])):
                    self.set_cell(row_number, column_number, list_of_lists[row_number][column_number])

    def add_self_to_matrix(self, other_matrix):
        if (self.columns != other_matrix.columns) or (self.rows != other_matrix.rows):
            raise self.IncompatibleMatrixException
        else:
            returnmatrix = matrix(self.rows, self.columns)
            for row_number in range(self.rows):
                for column_number in range(self.columns):
                    returnmatrix.set_cell(row_number, column_number, self.get_cell(row_number, column_number)+other_matrix.get_cell(row_number, column_number))
            return returnmatrix

    def add_value_to_self(self, value):
        returnmatrix = matrix(self.rows, self.columns)
        for row_number in range(self.rows):
            for column_number in range(self.columns):
                returnmatrix.set_cell(row_number, column_number, self.get_cell(row_number, column_number)+value)
        return returnmatrix

    def subtract_matrix_from_self(self, other_matrix):
        if (self.columns != other_matrix.columns) or (self.rows != other_matrix.rows):
            raise self.IncompatibleMatrixException
        else:
            returnmatrix = matrix(self.rows, self.columns)
            for row_number in range(self.rows):
                for column_number in range(self.columns):
                    returnmatrix.set_cell(row_number, column_number, self.get_cell(row_number, column_number)-other_matrix.get_cell(row_number, column_number))
            return returnmatrix

    def subtract_value_from_self(self, value):
        returnmatrix = matrix(self.rows, self.columns)
        for row_number in range(self.rows):
            for column_number in range(self.columns):
                returnmatrix.set_cell(row_number, column_number, self.get_cell(row_number, column_number)-value)
        return returnmatrix
        
    def multiply_self_by_value(self, value):
        returnmatrix = matrix(self.rows, self.columns)
        for row_number in range(self.rows):
            for column_number in range(self.columns):
                returnmatrix.set_cell(row_number, column_number, self.get_cell(row_number, column_number)*value)
        return returnmatrix

    def multiply_self_by_matrix(self, other_matrix):
        if (self.columns != other_matrix.rows):
            raise self.IncompatibleMatrixException
        else:
            returnmatrix = matrix(self.rows, other_matrix.columns)
            for i in range(self.rows):
                for j in range(other_matrix.columns):
                    temp = 0
                    for k in range(self.columns):
                        temp += self.get_cell(i, k)*other_matrix.get_cell(k, j)
                    returnmatrix.set_cell(i, j, temp)
            return returnmatrix

    ##finds a vector's magnitude
    def norm(self):
        return self.math.sqrt(self.get_cell(0,0)**2 + self.get_cell(1,0)**2 + self.get_cell(2,0)**2)
    
    ##normalizes a vector, any columns after the first
    ##will be ignored
    def normalize(self):
        norm = self.norm()
        if norm == 0: return self
        else: return self.multiply_self_by_value(1/norm)

        
    ##finds the cross product of twe vectors
    def cross(self, other):
        returnval = matrix(4, 1)
        returnval.set_entire_matrix([[self.get_cell(1, 0)*other.get_cell(2, 0) - self.get_cell(2, 0)*other.get_cell(1, 0)],
                           [self.get_cell(2, 0)*other.get_cell(0, 0) - self.get_cell(0, 0)*other.get_cell(2, 0)],
                           [self.get_cell(0, 0)*other.get_cell(1, 0) - self.get_cell(1, 0)*other.get_cell(0, 0)],
                           [1]])
        return returnval
        
    ##finds the dot product of two vectors
    def dot(self, other):
        return self.get_cell(0, 0)*other.get_cell(0, 0) + self.get_cell(1, 0)*other.get_cell(1, 0) + self.get_cell(2, 0)*other.get_cell(2, 0)

    def add(self, value):
        if isinstance(value, matrix):
            return self.add_self_to_matrix(value)
        else:
            return self.add_value_to_self(value)

    def multiply(self, value):
        if isinstance(value, matrix):
            return self.multiply_self_by_matrix(value)
        else:
            return self.multiply_self_by_value(value)

    def subtract(self, value):
        if isinstance(value, matrix):
            return self.subtract_matrix_from_self(value)
        else:
            return self.subtract_value_from_self(value)

