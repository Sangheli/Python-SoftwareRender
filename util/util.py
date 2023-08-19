import time


def get_time():
    return time.time()


def print_elapsed_time(st):
    et = time.time()
    elapsed_time = et - st
    print(elapsed_time * 1000, 'miliseconds')
