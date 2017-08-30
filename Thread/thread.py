import threading
import numpy as np
import time
import random


class ThreadPoll:
    def __init__(self, max_threads=None):
        self.max_theads = max_threads
        self.active_threads = []
        self.waiting = []
        self.lock = threading.Lock()
        self.count = 0

    def execute(self, method, args):
        # If we dont have a limit of threads, just start a new one
        if not self.max_theads:
            threading.Thread(target=method, args=args).start()
            self.count+=1
        else:
            # if we do have a limit of threads, then we must check if it is possible to start a new one
            # First we'll check if any thread already finished
            self.remove_finished_threads()

            # Adding thread to the end of waiting list
            self.waiting.append(threading.Thread(target=method, args=args))

            for thread in self.waiting:
                if len(self.active_threads) < self.max_theads:
                    self.waiting.remove(thread)
                    self.active_threads.append(thread)
                    thread.start()
                else:
                    # if we cant start a new thread
                    self.remove_finished_threads(wait=True)

    def remove_finished_threads(self, wait=None):
        to_remove = []
        for thread in self.active_threads:
            if not thread.isAlive():
                to_remove.append(thread)

        # if wait is True, it means that we cant start a new thread until a old one has been removed.
        # first we check if some thread already finished
        if to_remove:
            for thread in to_remove:
                self.active_threads.remove(thread)
        # if we couldnt remove any thread from the pool and wait is True, then we have to wait
        else:
            if wait:
                # we wait for the oldest thread added to the pool
                self.active_threads.pop().join()


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
            args = [line, line_index, column, column_index, result_matrix]
            thread_pool.execute(dot_product_vector, args)


def dot_product_vector(vector_1, i, vector_2, j, result_matrix):
    vector_1 = np.array(vector_1)
    vector_2 = np.array(vector_2)
    result_matrix[i, j] = np.dot(vector_1, vector_2)
    # time.sleep(random.random())

if __name__ == '__main__':
    matrix_a = np.random.randint(100, size=(100, 10))
    matrix_b = np.random.randint(100, size=(10, 100))

    lines_a, columns_a = matrix_a.shape
    lines_b, columns_b = matrix_b.shape

    result_matrix = np.ones((columns_b, lines_a))
    init = time.time()
    dot_product(matrix_a, matrix_b, result_matrix, max_threads=1000)
    print("thread took " + str(time.time()-init))

    init = time.time()
    product = np.dot(matrix_a, matrix_b)
    print("numpy took " + str(time.time() - init))

    # print("Validating result: ")
    # print(result_matrix)
    #
    # print(product)
