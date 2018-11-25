from threading import Thread
import Queue

class Transition(Thread)

    def __init__(self, M, N):
        super(Transition, self).__init__()
        self.M = M
        self.N = N
        self.inputs = [Queue.Queue(1)] * M
        self.outputs = [Queue.Queue(1)] * N

    def eligible(self):
        elig = True
        for queue in inputs:
            if queue.empty():
                elig = False
        return elig

    def fire(self):
        for queue in inputs:
            queue.get()
        for queue in outputs:
            queue.put(1)

    def run(self):
        while True:
            if self.eligible():
                self.fire()
