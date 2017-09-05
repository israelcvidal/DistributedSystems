import threading
import numpy as np
import time
import random


class ThreadPoll:
    def __init__(self, max_threads=None):
        self.max_threads = max_threads
        self.waiting = []
        self.lock = threading.Lock()
        # count is used to make sure we dont have more than the max of allowed threads.
        self.count = 0
        self.active_threads = []
        # condition is used to make sure all threads finished
        self.condition = threading.Event()

    def execute(self, method=None, args=None):
        # If we don''t have a limit of threads, just start a new one
        if not self.max_threads:
            thread = threading.Thread(target=method, args=args)
            self.active_threads.append(thread)
            thread.start()
        else:
            # if we do have a limit of threads, then we must check if it is possible to start a new one

            # Adding thread to the end of waiting list
            self.waiting.append(threading.Thread(target=method, args=args))

            self.execute_from_waiting()

    def execute_from_waiting(self):
            # we check if there is any thread in the waiting list and if we can initiate another one
            while self.waiting and self.count < self.max_threads:
                thread = self.increase_return_thread()
                if thread:
                    self.active_threads.append(thread)
                    thread.start()

    def increase_return_thread(self):
        # increment number of active threads and return a thread to be started
        with self.lock:
            if self.waiting:
                self.count += 1
                thread = self.waiting.pop()
                self.active_threads.append(thread)
            else:
                thread = None
        return thread

    def decrease(self, thread):
        with self.lock:
            self.count -= 1
            self.active_threads.remove(thread)
        # Execute a thread from the waiting list
        self.execute_from_waiting()
        # if after executing from waiting list we don' have any active threads, we can finish execution
        if not self.active_threads:
            self.condition.set()

    # wait all threads to finish
    def wait(self):
        self.condition.wait()


# calculate the product of two matrix using threads
def dot_product(_matrix_a, _matrix_b, _result_matrix, max_threads=None):
    _matrix_a = np.array(_matrix_a)
    _matrix_b = np.array(_matrix_b)

    # Validating sizes:
    _lines_a, _columns_a = _matrix_a.shape
    _lines_b, _columns_b = _matrix_b.shape

    if _columns_a != _lines_b:
        raise RuntimeError("Number of columns of _matrix_a and number of lines of _matrix_b must be the same!")

    thread_pool = ThreadPoll(max_threads)

    for line_index in range(_lines_a):
        line = _matrix_a[line_index, :]

        for column_index in range(_columns_b):
            column = _matrix_b[:, column_index]
            args = [line, line_index, column, column_index, _result_matrix, thread_pool]
            thread_pool.execute(dot_product_vector, args)
    # wait for all threads to finish
    thread_pool.wait()


# calculate dot product between two vectors
def dot_product_vector(vector_1, i, vector_2, j, _result_matrix, thread_pool=None):
    vector_1 = np.array(vector_1)
    vector_2 = np.array(vector_2)
    result = 0
    for index in range(len(vector_1)):
        result += vector_1[index] * vector_2[index]

    _result_matrix[i, j] = result
    if thread_pool:
        # call decrease so we know that the thread finished and can start a new one from waiting list
        thread_pool.decrease(threading.current_thread())
    # to see a real difference using single and multi threaded, remove comment from line below
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
    matrix_a = np.random.randint(10, size=(100, 100))
    matrix_b = np.random.randint(10, size=(100, 100))

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
