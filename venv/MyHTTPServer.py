import socket
import select
import configparser
import os
from HTTPCodes import  HTTPCodes


ROOT = "./site"
INDEX_FILE = "index.html"
FILE_NOT_FOUND = "404.html"
METHOD_NOT_SUPPORTED = "501.html"

class MyHTTPServer:
  def __init__(self, host, port):
    self.host = host
    self.port = port

  def serveForever(self):
    s = socket.socket(socket.AF_INET,
                    socket.SOCK_STREAM)
    print ('Socket created')
    try:
      s.bind((self.host,self.port))
    except socket.error as msg:
      print('Bind failed. Error Code: ' + str(msg[0]) + 'Message' + msg[1])
      sys.exit()

    print ('Socket bind completed')

    s.listen(10)
    print ('Socket now listening')

    while 1:
      conn, addr = s.accept()
      print ('Connected with ' + addr[0] + ':' + str(addr[1]))
      conn.setblocking(0)
      ready, _, _ = select.select([conn], [], [], 0.05)
      if ready:
        data = conn.recv(1024)
        print (data.decode())
        while True:
          ready, _, _ = select.select([conn], [], [], 0.05)
          if ready:
            data += conn.recv(1024)
          else:
            break


  def createResponse(self, HTTPCodes, ):
