import threading
import os,signal,sys
from time import sleep
from thread_watcher import Watcher

class Watcher2():  
  
    def __init__(self):  
        self.child = os.fork()  
        if self.child == 0:  
            return  
        else:  
            self.watch()  
  
    def watch(self):  
        try:  
            os.wait()  
        except KeyboardInterrupt:  
            self.kill()  
        sys.exit()  
  
    def kill(self):  
        try:  
            os.kill(self.child, signal.SIGKILL)  
        except OSError:  
            pass  


def test(n):
    for i in range(n):
        print i
        sleep(1)


def main():
    cnt = 10
    threads = []
    for i in range(2):
        t = threading.Thread(target=test,
                             args=(cnt,))
        threads.append(t)

    for i in range(2):
        threads[i].start()

    for i in range(2):
        threads[i].join()

if __name__ == '__main__':
    Watcher()
    main()
