from recvfile import recvImage
from thread_watcher import Watcher
import threading
from time import sleep,ctime

def test_fun():
	while True:
		print ctime()
		sleep(5)

def main():
    threads = []
    rc = threading.Thread(target=recvImage)
    ts = threading.Thread(target=test_fun)
    rc.start()
    ts.start()
    rc.join()
    ts.join()

if __name__ == '__main__':
	Watcher()
	main()
	
