"""
filename: matrix-multiplication.py
Matrix multiplication for n x n matrices.
"""


def matrix_addition(x, y):
    "adds two matrices together"
    assert len(x) > 0 and len(y) > 0 and len(
        x[0]) > 0 and len(y[0]) > 0, "Invalid matrices"
    assert len(x) == len(y) and len(x[0]) == len(
        y[0]), "matrix sizes do not match"
    rows = len(x)
    cols = len(x[0])
    c = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            c[i][j] = x[i][j] + y[i][j]
    return c


def matrix_subtraction(x, y):
    "subtracts matrix x - y"
    assert len(x) > 0 and len(y) > 0 and len(
        x[0]) > 0 and len(y[0]) > 0, "Invalid matrices"
    assert len(x) == len(y) and len(x[0]) == len(
        y[0]), "matrix sizes do not match"
    rows = len(x)
    cols = len(x[0])
    c = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            c[i][j] = x[i][j] - y[i][j]
    return c


def brute_matrix_mult(x, y):
    """brute force implementation of matrix multiplication"""
    assert len(x) > 0 and len(x[0]) > 0 and len(
        y) > 0 and len(y[0]) > 0, "Invalid matrices, either x or y have no rows"
    assert len(x[0]) == len(
        y), "Invalid size for matrices, cols of x must match the size of rows of y"

    x_rows = len(x)
    y_rows = len(y)
    y_cols = len(y[0])

    c = [[0 for _ in range(y_cols)] for _ in range(x_rows)]
    for i in range(x_rows):
        for j in range(y_cols):
            for k in range(y_rows):
                c[i][j] += x[i][k] * y[k][j]
    return c


def split_matrix(m, row_split, col_split, rows):
    """splits the matrix into 4 matrices"""
    a = []
    b = []
    c = []
    d = []
    for i in range(rows):
        if i < row_split:
            a.append(m[i][:col_split])
            b.append(m[i][col_split:])
        else:
            c.append(m[i][:col_split])
            d.append(m[i][col_split:])

    return a, b, c, d


def merge_quadrants(top_left, top_right, bottom_left, bottom_right):
    """Merges the 4 quadrants of a matrix into one matrix"""
    assert len(top_left) == len(
        top_right), "the top half do not match number of rows"
    assert len(bottom_left) == len(
        bottom_right), "the bottom half do not match number of rows"
    top_half = len(top_left)
    bottom_half = len(bottom_left)
    m = []
    for i in range(top_half):
        m.append(top_left[i] + top_right[i])
    for i in range(bottom_half):
        m.append(bottom_left[i] + bottom_right[i])
    return m


def recursive_matrix_mult(x, y):
    """naive recusrive matrix multiplication"""
    if len(x) == 1 or len(x[0]) == 1 or len(y) == 1 or len(y[0]) == 1:
        return brute_matrix_mult(x, y)
    else:
        half_x_row = len(x) // 2
        half_x_col = len(x[0]) // 2
        half_y_row = len(y) // 2
        half_y_col = len(y[0]) // 2
        a, b, c, d = split_matrix(x, half_x_row, half_x_col, len(x))
        e, f, g, h = split_matrix(y, half_y_row, half_y_col, len(y))

        ae = recursive_matrix_mult(a, e)
        bg = recursive_matrix_mult(b, g)
        ce = recursive_matrix_mult(c, e)
        dg = recursive_matrix_mult(d, g)
        af = recursive_matrix_mult(a, f)
        bh = recursive_matrix_mult(b, h)
        cf = recursive_matrix_mult(c, f)
        dh = recursive_matrix_mult(d, h)

        first_quadrant = matrix_addition(ae, bg)
        second_quadrant = matrix_addition(af, bh)
        third_quadrant = matrix_addition(ce, dg)
        fourth_quadrant = matrix_addition(cf, dh)

        return merge_quadrants(first_quadrant, second_quadrant, third_quadrant, fourth_quadrant)


def strassen_matrix_mult(x, y):
    """strassen method of matrix multiplication of 2n matrices"""
    assert len(x) > 0 and len(x[0]) > 0 and len(
        y) > 0 and len(y[0]) > 0, "invalid input for matrices"
    if len(x) == 1 or len(x[0]) == 1 or len(y) == 1 or len(y[0]) == 1:
        return brute_matrix_mult(x, y)
    else:
        assert len(x) % 2 == 0 and len(x[0]) % 2 == 0 and len(y) % 2 == 0 and len(
            y[0]) % 2 == 0, "invalid matrices for strassen's algorithm. Matrices must be of size 2n"
        half_x_row = len(x) // 2
        half_x_col = len(x[0]) // 2
        half_y_row = len(y) // 2
        half_y_col = len(y[0]) // 2

        a, b, c, d = split_matrix(x, half_x_row, half_x_col, len(x))
        e, f, g, h = split_matrix(y, half_y_row, half_y_col, len(y))

        p1 = strassen_matrix_mult(a, matrix_subtraction(f, h))
        p2 = strassen_matrix_mult(matrix_addition(a, b), h)
        p3 = strassen_matrix_mult(matrix_addition(c, d), e)
        p4 = strassen_matrix_mult(d, matrix_subtraction(g, e))
        p5 = strassen_matrix_mult(matrix_addition(a, d), matrix_addition(e, h))
        p6 = strassen_matrix_mult(
            matrix_subtraction(b, d), matrix_addition(g, h))
        p7 = strassen_matrix_mult(
            matrix_subtraction(a, c), matrix_addition(e, f))

        first_quadrant = matrix_addition(
            matrix_subtraction(matrix_addition(p5, p4), p2), p6)
        second_quadrant = matrix_addition(p1, p2)
        third_quadrant = matrix_addition(p3, p4)
        fourth_quadrant = matrix_subtraction(
            matrix_subtraction(matrix_addition(p1, p5), p3), p7)

        return merge_quadrants(first_quadrant, second_quadrant, third_quadrant, fourth_quadrant)


def main():
    """main function"""
    a = [[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 4]]
    b = [[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 4]]
    c = brute_matrix_mult(a, b)
    p = recursive_matrix_mult(a, b)
    s = strassen_matrix_mult(a, b)

    for i in c:
        for j in i:
            print(f"{j}", end=" ")
        print()
    print("----")
    for i in p:
        for j in i:
            print(f"{j}", end=" ")
        print()
    print("----")
    for i in s:
        for j in i:
            print(f"{j}", end=" ")
        print()


if __name__ == "__main__":
    main()
