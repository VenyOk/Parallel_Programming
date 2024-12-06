import threading
import time
import numpy as np


def count_live_neighbors(matrix, x, y, rows, cols):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    live_neighbors = 0
    for dx, dy in directions:
        nx, ny = (x + dx) % rows, (y + dy) % cols
        live_neighbors += matrix[nx][ny]
    return live_neighbors


def evolve_cell(matrix, new_matrix, x, y, rows, cols):
    live_neighbors = count_live_neighbors(matrix, x, y, rows, cols)
    if matrix[x][y] == 1:
        if live_neighbors < 2 or live_neighbors > 3:
            new_matrix[x][y] = 0
        else:
            new_matrix[x][y] = 1
    else:
        if live_neighbors == 3:
            new_matrix[x][y] = 1
        else:
            new_matrix[x][y] = 0


def worker(thread_id, matrix, new_matrix, rows, cols, num_threads, barrier):
    start_row = thread_id * (rows // num_threads)
    end_row = (thread_id + 1) * (rows // num_threads) if thread_id != num_threads - 1 else rows
    for x in range(start_row, end_row):
        for y in range(cols):
            evolve_cell(matrix, new_matrix, x, y, rows, cols)
    barrier.wait()


def main():
    rows, cols = 100, 100
    num_threads = 8
    num_steps = 10

    matrix = np.random.randint(2, size=(rows, cols))
    new_matrix = np.zeros((rows, cols), dtype=int)

    barrier = threading.Barrier(num_threads)

    start_time = time.time()
    for step in range(num_steps):
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=worker, args=(i, matrix, new_matrix, rows, cols, num_threads, barrier))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        matrix, new_matrix = new_matrix, matrix

    end_time = time.time()
    average_time_per_step = (end_time - start_time) / num_steps
    print(f"Среднее время выполнения одного шага с использованием потоков: {average_time_per_step:.6f} секунд")

    matrix = np.random.randint(2, size=(rows, cols))
    new_matrix = np.zeros((rows, cols), dtype=int)

    start_time = time.time()
    for step in range(num_steps):
        for x in range(rows):
            for y in range(cols):
                evolve_cell(matrix, new_matrix, x, y, rows, cols)
        matrix, new_matrix = new_matrix, matrix

    end_time = time.time()
    average_time_per_step_no_threads = (end_time - start_time) / num_steps
    print(f"Среднее время выполнения одного шага без использования потоков: {average_time_per_step_no_threads:.6f} секунд")


if __name__ == "__main__":
    main()
