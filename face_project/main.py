#!python3
from mythread import MyThread
from socket import *
from recvfile import recvImage,recvInit
from thread_watcher import Watcher
import threading
from recognize_face import encoding_image, recognize_image

def connect_from(tcpSer):
	tcpCli, addr = tcpSer.accept()
	print('-*- accpet one socket request:',addr)
	return tcpCli,True

def main():
	socket_num = 3
	ser_pi  = socket(AF_INET, SOCK_STREAM)
	ser_esp = socket(AF_INET, SOCK_STREAM)
	ser_phe = socket(AF_INET, SOCK_STREAM)
	sockets = [
		ser_pi,
		ser_esp,
		ser_phe
	] 
	ports = [
		9000,#Pi
		3721,#ESP
		7777 #phe
	]
	flag_pi = False
	flag_esp = False
	flag_phone = False

	for i in range(socket_num):
		sockets[i].setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
		sockets[i].bind(('',ports[i]))
		sockets[i].listen(5)

	threads = []

	for i in range(socket_num):
		t = MyThread(target=connect_from,args=(sockets[i],))
		threads.append(t)

	for i in range(socket_num):
		threads[i].start()
		threads[i].join()	

	cli_pi, flag_pi = threads[0].get_result()
	cli_esp,flag_esp = threads[1].get_result()
	cli_phone,flag_phone = threads[2].get_result()
	clients = [cli_pi,cli_esp,cli_phone]
	while True:
		if flag_pi and flag_esp and flag_phone:
			break
	print('three sockets connected')
	known_faces = encoding_image()	
	print ('waiting for order:')
	server = recvInit()
	for i in range(socket_num):
		clients[i].send(bytes('off',encoding='utf-8'))
	while True:
		data = cli_phone.recv(1024)
		print(data)
		if data == bytes('open',encoding='utf-8'):
			cli_pi.send(bytes('start',encoding='utf-8'))	
			data = clients[0].recv(1024)
			print(data.decode('ascii'))
			recvImage(server)
			reg_result = recognize_image(data.decode('ascii'),known_faces=known_faces)
			print (reg_result)
			if reg_result:
				cli_esp.send(bytes('on',encoding='utf-8'))
			else:
				cli_esp.send(bytes('off',encoding='utf-8'))
		if data == bytes('close',encoding='utf-8'):
			cli_pi.send(bytes('close',encoding='utf-8'))
			for i in range(socket_num):
				clients[i].close()
				sockets[i].close()
			break


if __name__ == '__main__':
	Watcher()
	main()
	
