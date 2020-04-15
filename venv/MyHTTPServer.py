import socket
import select
import configparser
import os
from HTTPCodes import  HTTPCodes


ROOT = "./site"
INDEX_FILE = "index.html"
FILE_NOT_FOUND = "404.html"
METHOD_NOT_SUPPORTED = "501.html"
HTTPMethods = ["GET", "POST", "OPTIONS"]

class MyHTTPServer:
  def __init__(self, host, port):
    self.host = host
    self.port = port

  def serveForever(self):
    while 1:
      headres = {}
      data = b""
      s = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)
      print ('Socket created')
      try:
        s.bind((self.host,self.port))
      except socket.error as msg:
        print('Bind failed. Error Code: ' + str(msg[0]) + 'Message' + msg[1])
        sys.exit()

      print ('Socket bind completed')

      s.listen(1)
      print ('Socket now listening')
      conn, addr = s.accept()
      while 1:
        data += conn.recv(1024)
        if data.decode().endswith("\n"):
          print(data.decode())
          break
        if not data:
          conn.close()
          break
      print("1")
      if data != b"":
        headers = self.parseRequest(data)
        if headers["method"] not in HTTPMethods:
          print("HI!")
          conn.send(self.unknownMethod(headers))
        elif headers["method"] == HTTPMethods[0]:
          print(headers["url"])
          conn.send(self.processGet(headers))
      conn.close()

  def parseRequest(self, databyte):
    data_list = databyte.decode().split("\r\n")
    headers = {}
    headers["method"], headers["url"], headers["version"] = data_list[0].split()
    for header in data_list[1: ]:
      if header != "":
        header_name, header_value = header.split(": ")
        headers[header_name] = header_value
    return headers

  def unknownMethod(self, headers):
    answer_body = ""
    with open(os.path.join(ROOT , METHOD_NOT_SUPPORTED)) as badMethod:
      return (self.createResponse(HTTPCodes.NOT_IMPLEMENTED.value, "".join(badMethod.readlines()), headers))


  def processGet(self, headers):
    answer_body = ""
    if headers["url"] in ["/", "/index", "/index.html", "index.html"]:
      with open(os.path.join(ROOT, INDEX_FILE)) as indexFile:
        return (self.createResponse(HTTPCodes.OK.value, "".join(indexFile.readlines()), headers))
    else:
      path = os.path.join(*headers["url"].split("/")[1:])
      with open(os.path.join(ROOT, path)) as file:
        return (self.createResponse(HTTPCodes.OK.value, "".join(file.readlines()), headers))

  def processPost(self):
    pass

  def processOptions(self):
    pass

  def createResponse(self, code, body, headers):

    answer_headers = "{version} {status_code} \n{headers}\n\n"\
      .format(version=headers["version"], status_code = code, headers ="")
    answer_body = body
    answer = answer_headers + answer_body
    return answer.encode()