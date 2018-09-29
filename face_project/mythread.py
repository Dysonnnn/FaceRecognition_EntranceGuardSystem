from  threading import Thread

class MyThread(Thread):
	def __init__(self,target=None,args=()):
		Thread.__init__(self)
		self.__target = target
		self.__args = args

	def run(self):
		self.result = self.__target(*self.__args)

	def get_result(self):
		return self.result
