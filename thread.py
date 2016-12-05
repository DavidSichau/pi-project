from threading import Thread

class InputProcessor:
    def __init__(self, queue):
        Thread.__init__(self)
        self.