from Queue import Queue
from threading import Thread
from time import time
from OptimizedGameManager import GameManager

results = []
class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            m = self.queue.get()
            y = m.start()
            results.append(y)
            self.queue.task_done()

def main():
    ts = time()
    managers = [GameManager("g{0:d}".format(i)) for i in range(10)]
    queue = Queue()

    for x in range(4):
        worker = DownloadWorker(queue)
        worker.daemon = True
        worker.start()

    for mgr in managers:
        print "Queueing {}".format(mgr.log)
        queue.put(mgr)

    queue.join()
    print "Took {}".format(time()-ts)
    for result in results: print result

if __name__=="__main__":
    main()