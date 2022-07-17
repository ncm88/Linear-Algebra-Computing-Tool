class Grid: #Generic grid class

  def __init__(self, width, height):
      '''
      :param width: desired width of grid
      :param height: desired height of grid
      '''
      self.width = width
      self.height = height
      self.grid = []
      for x in range(self.width):
          column = []
          for y in range(self.height):
              column.append(None)
          self.grid.append(column)

  def setval(self, xcoord, ycoord, val):
      '''
      :param xcoord: x coordinate on grid
      :param ycoord: y coordinate on grid
      :param val: desired value to be set at given coordinates
      :return: method is a modifier only
      '''
      self.grid[xcoord][ycoord] = val

  def getval(self,xcoord,ycoord):
      '''
      :param xcoord: x coordinate on grid
      :param ycoord: y coordinate on grid
      :return: the value at the given x and y coordinates
      '''
      return self.grid[xcoord][ycoord]

  def __str__(self):
      mystr = ''
      for y in range(self.height):
          for x in range(self.width):
              mystr += str('{:.2f}'.format(self.getval(x, y)))
              mystr += '|'
          mystr += '\n'
      return mystr


class Matrix(Grid): #Specialized grid class with aditional matrix-specific operations

  def __add__(self, other):
      '''
      :param other: other matrix to add to the original matrix
      :return: the sum of the two matrices if possible
      '''
      if self.width == other.width and self.height == other.height:
          newmatrix = Matrix(self.width,self.height)
          for x in range(newmatrix.width):
              for y in range(newmatrix.height):
                   newmatrix.setval(x,y,(self.grid[x][y] + other.grid[x][y]))
          return newmatrix
      else:
          raise IndexError('Non-compatible matrices')

  def __sub__(self, other):
      '''
      :param other: other matrix to subtract from self
      :return: a matrix representing the difference between self and other if possible
      '''
      if self.width == other.width and self.height == other.height:
          newmatrix = Matrix(self.width, self.height)
          for x in range(newmatrix.width):
              for y in range(newmatrix.height):
                  newmatrix.setval(x,y,(self.grid[x][y] - other.grid[x][y]))
          return newmatrix
      else:
          raise IndexError('Non-compatible matrices')

  def matrix_mult(self, other):
      '''
      :param other: other matrix to multiply self
      :return: the product matrix of the two if possible
      '''
      newmatrix = Matrix(other.width, self.height)
      if self.width == other.height:
          for y in range(self.height):
              for n in range(other.width):
                  dotproduct = int()
                  for x in range(self.width):
                      dotproduct += self.grid[x][y]*other.grid[n][x]
                      newmatrix.setval(n, y, dotproduct)
          return newmatrix
      else:
          return IndexError('Non-compatible matrices')

  def scalar_mult(self, scalar):
      '''
      :param scalar: scalar value to multiply matrix by
      :return: a new matrix consisting of the product of the old matrix and scalar if possible
      '''
      newmatrix = Matrix(self.width,self.height)
      for y in range(self.height):
          for x in range(newmatrix.width):
              newmatrix.grid[x][y] *= scalar
      return newmatrix

  def is_square(self):
      '''
      :return: True if matrix is square False if not
      '''
      return self.height == self.width

  def swap_rows(self, row1, row2):
      '''
      :param row1: first row
      :param row2: other row
      :return: matrix with row 1 and row 2 positions swapped
      '''
      for x in range(self.width):
          self.grid[x][row1], self.grid[x][row2] = self.grid[x][row2], self.grid[x][row1]
      return self

  def mult_row(self, row, factor):
      '''
      :param row: row to multiply by factor
      :param factor: factor to multiply row
      :return: row * factor
      '''
      for x in range(self.width):
          self.grid[x][row] *= factor

  def div_row(self, row, factor):
      '''
      :param row: row to divide by factor
      :param factor: factor to divide row by
      :return: row/factor
      '''
      for x in range(self.width):
          self.grid[x][row] /= factor

  def elim(self, row1, row2, factor):
      '''
      row1 -= factor * row2
      :param row1: row to be subtracted from
      :param row2: row being subtracted
      :param factor: factor multiplying subtracting row
      :return: post row elim matrix
      '''
      for x in range(self.width):
          n = self.grid[x][row2]*factor
          self.grid[x][row1] -= n

  def merge_with_identity(self):
      '''
      :return: Original matrix with identity matrix injected afterwards
      '''
      identity = Matrix(self.width, self.height)
      columncount = 0
      for y in range(self.height):
          for x in range(self.width):
              if x == columncount:
                  identity.setval(x, y, 1)
              else:
                  identity.setval(x, y, 0)
          columncount += 1
      merger = Matrix(self.width*2, self.height)
      for y in range(merger.height):
          for x in range(merger.width):
              if x in range(self.width):
                  merger.setval(x,y,self.grid[x][y])
              else:
                  merger.setval(x,y,identity.grid[x-identity.width][y])
      return merger

  def gaussian_eliminator(self):
      '''
      :return: matrix after undergoing gaussian elimination
      '''
      self.handle_zeroes()
      columncounter = 0
      for i in range(self.height):
         self.div_row(i,self.grid[columncounter][i])
         columncounter+=1
         for j in range(self.height):
             if j != i:
                 self.elim(j,i,self.grid[i][j])

  def return_inverse(self):
      '''
      :return: the inverse matrix
      '''
      if self.is_invertable() is True:
          proto = self.merge_with_identity()
          proto.gaussian_eliminator()
          invmatrix = Matrix(self.width,self.height)
          for y in range(self.height):
              for x in range(self.width):
                  invmatrix.setval(x,y,proto.grid[x+self.width][y])
          return invmatrix
      raise ValueError('Un-invertable matrix')

  def is_invertable(self):
      '''
      :return: True if matrix is invertable, False if not
      '''
      for y in range(self.height):
          for x in range(self.width):
              if self.grid[x][y]==0:
                  return False
              return True

  def handle_zeroes(self):
      '''
      :return: The matrix re-arranged to accomodate gaussian elimination
      '''
      for i in range(self.height):
          if self.grid[i][i]==0:
              for j in range(self.height):
                  if self.grid[i][j]!=0:
                      self.swap_rows(i,j)
