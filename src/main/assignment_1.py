
import numpy as np
import numpy as np
def nevilles_method(x_points, y_points, x):
   
    matrix = np.zeros((len(x_points),len(x_points)))
    # fill in value (just the y values because we already have x set)
    for counter, row in enumerate(matrix):
        row[0] = y_points[counter]
    # the end of the first loop are how many columns you have...
    num_of_points = len(x_points)

    # the end of the second loop is based on the first loop...
    for i in range(1, num_of_points):
        for j in range(1, i+1):
            first_multiplication = (x - x_points[i-j]) * matrix[i][j-1]
            second_multiplication = (x - x_points[i]) * matrix[i-1][j-1]
            denominator = x_points[i] - x_points[i-j]
            # this is the value that we will find in the matrix
            coefficient = (first_multiplication-second_multiplication)/(denominator)
            matrix[i][j] = coefficient
    
    return matrix

def divided_difference_table(x_points, y_points):
    # set up the matrix
    size: int =len(x_points)
    matrix: np.array = np.zeros((size,size))
    # fill the matrix
    for index, row in enumerate(matrix):
        row[0] = y_points[index]
    # populate the matrix (end points are based on matrix size and max operations 
    for i in range(1, size):
        for j in range(1, i+1):
            # the numerator are the immediate left and diagonal left indices...
            numerator = matrix[i][j-1] - matrix[i-1][j-1]
            # the denominator is the X-SPAN...
            denominator =x_points[i]- x_points[i-j]
            operation = numerator / denominator
            # cut it off to view it more simpler
            matrix[i][j] = operation
    return matrix
def apply_div_dif(matrix: np.array):
    size = len(matrix)
    for i in range(2, size):
        for j in range(2, i+2):
            # skip if value is prefilled (we dont want to accidentally precalculate)
            if j >= len(matrix[i]) or matrix[i][j] != 0:
                continue
            
            # get left cell entry
            left: float = matrix[i][j-1]
            # get diagonal left entry
            diagonal_left: float = matrix[i-1][j-1]
            # order of numerator is SPECIFIC.
            numerator: float = left - diagonal_left
            # denominator is current i's x_val minus the starting i's x_val....
            denominator = matrix[i][0] - matrix[i-j+1][0]
            # something save into matrix
            operation = numerator / denominator
            matrix[i][j] = operation
    
    return matrix

def hermite_interpolation(x_points, y_points, slopes):
    # matrix size changes because of "doubling" up info for hermite 
    num_of_points = len(x_points)
    matrix = np.zeros((2*num_of_points, 2*num_of_points))
    # populate x values (make sure to fill every TWO rows)
    for x in range(num_of_points):
        matrix[x*2][0] = x_points[x]
        matrix[x*2+1][0] = x_points[x]
    
    # prepopulate y values (make sure to fill every TWO rows)
    for x in range(num_of_points):
        matrix[x*2][1] = y_points[x]
        matrix[x*2+1][1] = y_points[x]
    
    # prepopulate with derivates (make sure to fill every TWO rows. starting row 
    for x in range(num_of_points):
        matrix[x*2+1][2] = slopes[x]
    
    
    filled_matrix = apply_div_dif(matrix)
    print(filled_matrix)

def get_approximate_result(matrix, x_points, value):
    # p0 is always y0 and we use a reoccuring x to avoid having to recalculate x 
    # Line 51 , 54 and 57
    reoccuring_x_span = 1
    reoccuring_px_result = matrix[0][0]
    
    # we only need the diagonals...and that starts at the first row...
    for index in range(1,len(x_points)):
        polynomial_coefficient = matrix[index][index]
        # we use the previous index for x_points....
        reoccuring_x_span *= (value - x_points[ index-1])
        
        # get a_of_x * the x_span
        mult_operation = polynomial_coefficient * reoccuring_x_span
        # add the reoccuring px result
        reoccuring_px_result += mult_operation
    
    # final result
    return reoccuring_px_result

def cubic_spline_interpolation(x, y):
    n = len(x)
    h = [x[i+1]-x[i] for i in range(n-1)]

    # calculate the tridiagonal matrix
    tri_diag = [[0]*(n-2) for i in range(n-2)]
    for i in range(n-2):
        if i == 0:
            tri_diag[i][i] = 2*(h[i]+h[i+1])
            tri_diag[i][i+1] = h[i+1]
        elif i == n-3:
            tri_diag[i][i] = 2*(h[i]+h[i+1])
            tri_diag[i][i-1] = h[i]
        else:
            tri_diag[i][i-1] = h[i]
            tri_diag[i][i] = 2*(h[i]+h[i+1])
            tri_diag[i][i+1] = h[i+1]
    print(tri_diag)

def main():
    np.set_printoptions(precision=7, suppress=True, linewidth=100)
    entries_x = [3.6,3.8,3.9]
    entries_y = [1.675,1.436,1.318]
    entries_x2 = [7.2,7.4,7.5,7.6]
    entries_y2 = [23.5492,25.3913,26.8224,27.4589]
    entries_x3 = [3.6,3.8,3.9]
    entries_y3 = [1.675,1.436,1.318]

    entries_x4 = [2,5,8,10]
    entries_y4 =[3,5,7,9]
    slope = [-1.195,-1.188,-1.182]
    
    # PRINTOUT 1
    val = nevilles_method(entries_x,entries_y,3.700)
    print(val[2][2])
    # PRINTOUT 2
    matrix2 = divided_difference_table(entries_x2,entries_y2)
    threeVals = [matrix2[1][1],matrix2[2][2],matrix2[3][3]]
    print(threeVals)
    # PRINTOUT 3
    print(get_approximate_result(matrix2,entries_x2,7.3))
    # PRINTOUT 4
    hermite_interpolation(entries_x3,entries_y3,slope)
    # PRINTOUT 5
    cubic_spline_interpolation(entries_x4,entries_y4)




main()