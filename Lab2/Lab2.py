import time
from mpi4py import MPI
import numpy as np
from numpy.linalg import norm
import sys

np.random.seed(30)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

MATRIX_SIZE = int(2 ** 13)
MATRIX_SPLIT = int(sys.argv[1])

a = np.ones((MATRIX_SIZE, MATRIX_SIZE), dtype=np.double)
np.fill_diagonal(a, 2)

# Test 1
#b = np.ones(MATRIX_SIZE, dtype=np.double) * int(2 ** 13 + 1)

# Test 2
u = np.sin(2 * np.pi * np.arange(MATRIX_SIZE) / MATRIX_SIZE)
b = a @ u

x = np.zeros(MATRIX_SIZE, dtype=np.double)

EPS = 0.00001


def mult_matrix_by_vector(m, v):
    v = v[:, None]  # Преобразуем вектор в столбец для матричного умножения
    part_a = np.empty(shape=(MATRIX_SIZE // MATRIX_SPLIT, MATRIX_SIZE), dtype=np.double)

    # Распределяем части матрицы между процессами
    comm.Scatter(m, part_a, root=0)

    # Умножаем подматрицу на вектор
    part_a = part_a @ v

    # Сбор результата с разных процессов
    res = None
    if rank == 0:
        res = np.empty(shape=(MATRIX_SIZE, 1), dtype=np.double)

    comm.Gather(part_a, res, root=0)

    # Все процессы получают итоговый результат
    return comm.bcast(res, root=0).T[0]


def main():
    global x

    old_crit = 0
    i = 0
    while True:
        i += 1
        print(f'x = {x}')
        y = mult_matrix_by_vector(a, x) - b
        print(f'y = {y}')
        ay = mult_matrix_by_vector(a, y)

        flag = False
        if rank == 0:
            crit = norm(y) / norm(b)
            if crit < EPS or crit == old_crit:
                flag = True
            else:
                old_crit = crit
                tao = (y.dot(ay)) / (ay.dot(ay))
                x = x - tao * y

        if comm.bcast(flag, root=0):
            break
        x = comm.bcast(x, root=0)


if __name__ == '__main__':
    t = time.time()
    main()

    if rank == 0:
        t_end = time.time() - t
        print(f'Solution found in {t_end:.4f} seconds')
        print('Vector x:')
        print(x)

        with open('stats.txt', 'a') as f:
            f.write(f'{MATRIX_SPLIT} {t_end}\n')
