import socket
import threading
import os
import sys
import math

def progressbar(cur, total):
    percent = '{:.2%}'.format(float(cur) / float(total))
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s" % (
                            '=' * int(math.floor(cur * 50 / total)),
                            percent))
    sys.stdout.flush()

 
def checkFileName(originalFileName):
    extensionIndex = originalFileName.rindex(bytes(".",encoding='utf-8'))
    name = originalFileName[:extensionIndex]
    extension = originalFileName[extensionIndex+1:]
    
    index = 1
    newNameSuffix = "(" + str(index) + ")"
    finalFileName = originalFileName
    if os.path.exists(finalFileName):
        finalFileName = name + " " + newNameSuffix + "." + extension
    while os.path.exists(finalFileName):
        index += 1
        oldSuffix = newNameSuffix
        newNameSuffix = "(" + str(index) + ")"
        finalFileName = finalFileName.replace(oldSuffix, newNameSuffix)
    return finalFileName

def handleClient(clientSocket):
    # receive file size
    fileSize = int(clientSocket.recv(1024))
    # print "[<==] File size received from client: %d" % fileSize
    clientSocket.send(bytes("Received",encoding='utf-8'))
    # receive file name
    fileName = clientSocket.recv(1024)
    # print "[<==] File name received from client: %s" % fileName
    clientSocket.send(bytes("Received",encoding='utf-8'))
    fileName = checkFileName(fileName)
    file = open(fileName, 'wb')
    # receive file content
    print ("[==>] Saving file to %s" % fileName)
    receivedLength = 0
    while receivedLength < fileSize:
        bufLen = 1024
        if fileSize - receivedLength < bufLen:
            bufLen = fileSize - receivedLength
        buf = clientSocket.recv(bufLen)
        file.write(buf)
        receivedLength += len(buf)
        process = int(float(receivedLength) / float(fileSize) * 100)
        progressbar(process, 100)
    
    file.close()
    print ("\r\n[==>] File %s saved." % fileName)
    clientSocket.send(bytes("Received",encoding='utf-8'))
    clientSocket.close()

def recvInit():
    bindIp = "0.0.0.0"
    bindPort = 8426

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind((bindIp, bindPort))
    server.listen(5)
    print ("Listening on %s:%d" % (bindIp, bindPort))
    return server

def recvImage(server):
        client, addr = server.accept()
        print ("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))
        handleClient(client)
    
