import threading
import numpy as np
import time
import random


class ThreadPoll:
    def __init__(self, max_threads=None):
        self.max_threads = max_threads
        self.waiting = []
        self.lock = threading.Lock()
        self.count = 0
        self.active_threads = []

    def execute(self, method=None, args=None):
        # If we dont have a limit of threads, just start a new one
        if not self.max_threads:
            thread = threading.Thread(target=method, args=args)
            self.actived_threads.append(thread)
            thread.start()
        else:
            # if we do have a limit of threads, then we must check if it is possible to start a new one

            # Adding thread to the end of waiting list
            self.waiting.append(threading.Thread(target=method, args=args))

            self.execute_from_waiting()

    def execute_from_waiting(self):
            while self.waiting and self.count < self.max_threads:
                thread = self.increase_return_thread()
                if thread:
                    self.actived_threads.append(thread)
                    thread.start()

    def increase_return_thread(self):
        with self.lock:
            if self.waiting:
                self.count += 1
                thread = self.waiting.pop()
                self.actived_threads.append(thread)
            else:
                thread = None
        return thread

    def decrease(self, thread):
        with self.lock:
            self.count -= 1
            self.actived_threads.remove(thread)
        # Execute a thread from the waiting list
        self.execute_from_waiting()


# product of two matrixes using threads
def dot_product(matrix_a, matrix_b, result_matrix, max_threads=None):
    matrix_a = np.array(matrix_a)
    matrix_b = np.array(matrix_b)

    # Validating sizes:
    lines_a, columns_a = matrix_a.shape
    lines_b, columns_b = matrix_b.shape

    if columns_a != lines_b:
        raise RuntimeError("Number of columns of matrix_a and number of lines of matrix_b must be the same!")

    thread_pool = ThreadPoll(max_threads)

    for line_index in range(lines_a):
        line = matrix_a[line_index, :]

        for column_index in range(columns_b):
            column = matrix_b[:, column_index]
            args = [line, line_index, column, column_index, result_matrix, thread_pool]
            thread_pool.execute(dot_product_vector, args)


# calculate dot product between two vectors
def dot_product_vector(vector_1, i, vector_2, j, _result_matrix, thread_pool=None):
    vector_1 = np.array(vector_1)
    vector_2 = np.array(vector_2)
    result = 0
    for index in range(len(vector_1)):
        result += vector_1[index] * vector_2[index]

    # print("antes ", _result_matrix[i, j])
    _result_matrix[i, j] = result
    # print("depois ", _result_matrix[i, j])
    if thread_pool:
        thread_pool.decrease()
    # time.sleep(random.random())


# Just to compare with single threaded
def dot_product_matrix(_matrix_a, _matrix_b, _result_matrix):
    _matrix_a = np.array(_matrix_a)
    _matrix_b = np.array(_matrix_b)

    # Validating sizes:
    _lines_a, _columns_a = _matrix_a.shape
    _lines_b, _columns_b = _matrix_b.shape

    if _columns_a != _lines_b:
        raise RuntimeError("Number of columns of matrix_a and number of lines of matrix_b must be the same!")

    for line_index in range(_lines_a):
        line = _matrix_a[line_index, :]

        for column_index in range(_columns_b):
            column = _matrix_b[:, column_index]
            dot_product_vector(line, line_index, column, column_index, _result_matrix, thread_pool=None)

if __name__ == '__main__':
    # generating 2 random matrix
    matrix_a = np.random.randint(10, size=(10, 10))
    matrix_b = np.random.randint(10, size=(10, 10))

    lines_a, columns_a = matrix_a.shape
    lines_b, columns_b = matrix_b.shape

    result_matrix = np.ones((columns_b, lines_a))
    init = time.time()
    dot_product(matrix_a, matrix_b, result_matrix, max_threads=None)
    finish = time.time()

    print("matrix_a: ")
    print(matrix_a)

    print("\nmatrix_b:")
    print(matrix_b)

    print("\nproduct:")
    print(result_matrix)
    print("\ncalculation took " + str(time.time()-init))

    result_matrix_without_thread = np.ones((columns_b, lines_a))
    init = time.time()
    dot_product_matrix(matrix_a, matrix_b, result_matrix_without_thread)
    print("single threaded took " + str(time.time()-init))
