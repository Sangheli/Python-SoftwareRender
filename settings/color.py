import numpy as np

black = (20, 20, 20)
blackTrue = (0, 0, 0)
white = (230, 230, 230)


def get_random(): return list(np.random.choice(range(256), size=3))
