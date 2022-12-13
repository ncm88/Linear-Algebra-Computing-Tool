import matrix

def create_matrix():
   width = 0
   height = 0
   while True:
       try:
           width = int(input('ENTER DESIRED MATRIX WIDTH \n'))
       except Exception:
           print('INVALID INPUT \n')
           continue
       if width > 0:
           break
       else:
           print('INVALID INPUT \n')
   while True:
       try:
           height = int(input('ENTER DESIRED MATRIX HEIGHT \n'))
       except Exception:
           print('INVALID INPUT \n')
           continue
       if height > 0:
           break
       else:
           print('INVALID INPUT \n')

   genmatrix = matrix.Matrix(width,height)
   for y in range(genmatrix.height):
       for x in range(genmatrix.width):
           while True:
               try:
                   value = int(input(('ENTER VALUE FOR ROW %d COLUMN %d\n' % (y,x))))
                   genmatrix.setval(x,y,value)
                   break
               except Exception:
                   print('INVALID INPUT \n')
   return genmatrix


def operationselect(givenmatrix):
   setofoperations = {'setval', 'getval', 'matrix_mult', 'scalar_mult', 'is_square', 'swap_rows', 'mult_row', 'div_row', 'elim', 'merge_with_identity', 'gaussian_eliminator', 'return_inverse', 'is_invertable', 'handle_zeroes'}
   while True:
       try:
           desiredoperation = str(input('CHOOSE AN OPERATION \n'))
           if desiredoperation in setofoperations:
               if desiredoperation=='setval':


           else:
               print('INVALID operation \n')
