import time
from random import randint
import multiprocessing as mp
import matplotlib.pyplot as plt

size = 400
processes_num = 0


def random_matrix():
    return [[randint(0, 3) for i in range(size)] for j in range(size)]


def matrix_prod(A, B):
    C = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            C[i][j] = sum(A[i][k] * B[k][j] for k in range(size))
    return C


def matrix_prod2(A, B):
    C = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            C[j][i] = sum(A[j][k] * B[k][i] for k in range(size))
    return C


def equal_matrices(A, B):
    for i in range(size):
        for j in range(size):
            if A[i][j] != B[i][j]:
                return False
    return True


def print_matrix(M):
    for i in range(size):
        for j in range(size):
            print(M[i][j], end=' ')
        print()


def compute_row(args):
    i, A, B = args
    row = [0] * size
    for j in range(size):
        row[j] = sum(A[i][k] * B[k][j] for k in range(size))
    return row


def parallel_matrix_prod(A, B):
    with mp.Pool(processes=processes_num) as pool:
        args = [(i, A, B) for i in range(size)]
        rows = pool.map(compute_row, args)
    return rows


if __name__ == "__main__":
    M = random_matrix()
    N = random_matrix()
    x = []
    y = []
    y2 = []
    for i in range(1, mp.cpu_count() + 4):
        processes_num = i
        x.append(i)
        start = time.time()
        C_parallel = parallel_matrix_prod(M, N)

        end = time.time()
        # print_matrix(C_parallel)
        print(end - start)
        y2.append(end - start)
        start2 = time.time()

        C = matrix_prod2(M, N)
        end2 = time.time()
        # print_matrix(C)
        print(end2 - start2)
        y.append(end2 - start2)
        print(equal_matrices(C_parallel, C))

    plt.plot(x, y, color='red', marker='o', markersize=7)
    plt.xlabel('Номер замера')
    plt.ylabel('Время')
    plt.title('Непараллельный алгоритм')
    plt.show()

    plt.plot(x, y2, color='red', marker='o', markersize=7)
    plt.xlabel('Количество потоков')
    plt.ylabel('Время')
    plt.title('Параллельный алгоритм')
    plt.show()
