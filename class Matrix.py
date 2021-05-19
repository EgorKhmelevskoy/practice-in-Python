def det(mat):
    if len(mat) > 2:
        alg = list(enumerate(mat[0]))
        alg = list(map(lambda x: x[1] * ((-1) ** (x[0] + 2)), alg))
        minors = list(enumerate([mat[1:]] * len(alg)))
        minors = list(map(lambda x: list(map(lambda y: list(y[:x[0]] + y[x[0] + 1:]), x[1])), minors))
        return sum(list(map(lambda x, y: x * y, list(map(lambda z: det(z), minors)), alg)))
    else:
        return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]


class MatrixError(BaseException):
    def __init__(self, matrix1, matrix2=None):
        if isinstance(matrix2, Matrix):
            self.arg1 = matrix1
            self.arg2 = matrix2
            self.ncol1 = len(matrix1.data[0])
            self.nrow1 = len(matrix1.data)
            self.ncol2 = len(matrix2.data[0])
            self.nrow2 = len(matrix2.data)
        else:
            self.arg = matrix1
            self.ncol = len(matrix1.data[0])
            self.nrow = len(matrix1.data)

class Matrix:
    def __init__(self, data):
        lenrows = list(map(lambda x: len(x), data))
        longrow = max(lenrows)
        if any(list(map(lambda x: x != longrow, lenrows))):
            for i in range(len(data)):
                if len(data[i]) != longrow:
                    data[i].extend([0] * (longrow - len(data[i])))
        self.data = data[:]

    def transpose(self):
        transMat = []
        for i in range(len(self.data[0])):
            row = list(map(lambda x: x[i], self.data))
            transMat.append(row)
        self.data = transMat
        return self

    @staticmethod
    def det(mat):
        if isinstance(mat, Matrix) and all(list(map(lambda x: len(x) == len(mat.data), mat.data))):
            return det(mat.data)
        else:
            return 'У матрицы данной размерности нельзя вычислить определитель'

    @staticmethod
    def transposed(x):
        return Matrix(x.data).transpose()

    def size(self):
        return len(self.data), len(self.data[1])

    def solve(self, free):
        determinant = det(self.data)
        if determinant == 0 or not isinstance(determinant, int):
            raise MatrixError(self)
        else:
            roots = []
            size = len(self.data)
            for i in range(size):
                minor = list(map(lambda x: x[:], self.data))
                for j in range(size):
                    minor[j][i] = free[j]
                root = det(minor) / determinant
                roots.append(root)
            return roots

    def __str__(self):
        mat = ''
        for i in range(len(self.data)-1):
            mat += (str(self.data[i])[1:-1].replace(', ', '\t') + '\n')
        mat += str(self.data[-1])[1:-1].replace(', ', '\t')
        return mat

    def __add__(self, other):
        if isinstance(self.data, list) and isinstance(other.data, list) and list(map(lambda x: (self.data.index(x), len(x)), self.data)) == list(map(lambda x: (other.data.index(x), len(x)), other.data)):
            result = list(map(lambda x, y: list(zip(x, y)), self.data, other.data))
            result = Matrix(list(map(lambda x: list(map(lambda y: y[0] + y[1], x)), result)))
            return result
        else:
            raise MatrixError(self, other)

    def __mul__(self, other):
        if all([isinstance(self, Matrix), isinstance(other, Matrix)]) and all(list(map(lambda x: len(x) == len(other.data), self.data))):
            result = []
            for i in self.data:
                row = []
                for j in range(len(other.data[0])):
                    element = sum(list(map(lambda x: x[0] * x[1], list(zip(i, list(map(lambda x: x[j], other.data)))))))
                    row.append(element)
                result.append(row)
            result = Matrix(result)
        elif any([isinstance(other, float), isinstance(other, int)]):
            result = Matrix(list(map(lambda x: list(map(lambda y: y * other, x)), self.data)))
        else:
            raise MatrixError(self, other)
        return result

    __rmul__ = __mul__

class PowMatrix(Matrix):
    def __pow__(self, power, modulo=None):
        if self.size()[0] == self.size()[1]:
            result = []
            for i in range(len(self.data)):
                row = [0] * len(self.data)
                row[i] = 1
                result.append(row)
            result = Matrix(result)
            twosys = list(map(int, bin(power)[2:].replace('', ' ').split(' ')[1:-1]))
            twosys.reverse()
            factor = Matrix(self.data)
            for i in twosys:
                if i:
                    result *= factor
                factor *= factor
            return result
        else:
            raise MatrixError(self)



b = [[-10, 20, 50, 2443], [-5235, 12, 4324, 4234]]
a = PowMatrix(b)

print(MatrixError(a).arg)

c = Matrix([[1,2], [3,4]])
d = Matrix([[0,1, 5], [1, 0]])
m = Matrix([[1, 1, 1]])

try:
    print(c + m)
except MatrixError as ce:
    print('Matrices have different dimensions or error in args:', ce.arg1, ce.arg2)
try:
    print(d * c)
except MatrixError as mull:
    print('Number of columns of the first matrix: ',mull.ncol1, ', does not match number of rows of the second matrix: ', mull.nrow2, sep='')

f = Matrix([[2, 3, 0, 4, 5], [0, 1, 0, -1, 2], [3, 2, 1, 0, 1],[0, 4 , 0 , -5, 0], [1, 1, 2, -2, 1]])

print(Matrix.det(f))
print(*Matrix([[2,1,1], [1,-1,0], [3,-1]]).solve([2, -2, 2]))
print(*c.solve([6,7]))

try:
    print(PowMatrix([[1, -1, 0], [3, -1, 2]]) ** 0)
except MatrixError as pow:
    print('Матрицу данной размерности: ', pow.nrow, ' * ', pow.ncol, ' - нельзя возводить в степень', sep='')

m = PowMatrix([[1, 1, 0, 0, 0, 0],
                  [0, 1, 1, 0, 0, 0],
                  [0, 0, 1, 1, 0, 0],
                  [0, 0, 0, 1, 1, 0],
                  [0, 0, 0, 0, 1, 1],
                  [0, 0, 0, 0, 0, 1]]
                )
print(m)
print('----------')
print(m ** 1)
print('----------')
print(m ** 2)
print('----------')
print(m ** 3)
print('----------')
print(m ** 4)
print('----------')
print(m ** 5)