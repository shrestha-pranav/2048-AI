from multiprocessing import Pool
from OptimizedGameManager import GameManager
from time import time

def f(x):
    g = GameManager("g{0:d}".format(x))
    res = g.start()
    return res

if __name__ == '__main__':
    ts = time()
    p = Pool(4)
    print p.map(f, range(12))
    print "Took {}".format(time()-ts)