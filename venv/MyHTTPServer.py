import socket
import os
import time
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
    s = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)
    print('Socket created')
    try:
      s.bind((self.host, self.port))
    except socket.error as msg:
      print('Bind failed. Error Code: ' + str(msg[0]) + 'Message' + msg[1])
      sys.exit()

    print('Socket bind completed')
    s.listen(10)
    print('Socket now listening')

    while 1:
      headres = {}
      data = b""
      conn, addr = s.accept()
      while 1:
        data += conn.recv(1024)
        print(data.decode())
        if data.decode().endswith("\n"):
          break
        if not data:
          conn.close()
          break
      if data != b"":
        try:
          headers = self.parseRequest(data)
          if headers["method"] not in HTTPMethods:
            conn.send(self.unknownMethod(headers))
          elif headers["method"] == HTTPMethods[0]:
            print(headers["url"])
            conn.send(self.processGet(headers))
          elif headers["method"] == HTTPMethods[1]:
            conn.send(self.processPost(headers))
          elif headers["method"] == HTTPMethods[2]:
            conn.send(self.processOptions(headers))
        except FileNotFoundError:
          conn.send(self.fileNotFound(headers))
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
      return (self.createResponse(HTTPCodes.NOT_IMPLEMENTED.value, "".join(badMethod.readlines()), "Not Implemented", headers))


  def processGet(self, headers):
    answer_body = ""
    if headers["url"] in ["/", "/index", "/index.html", "index.html"]:
      with open(os.path.join(ROOT, INDEX_FILE)) as indexFile:
        return (self.createResponse(HTTPCodes.OK.value, "".join(indexFile.readlines()), "OK", headers))
    else:
      path = os.path.join(*headers["url"].split("/")[1:])
      with open(os.path.join(ROOT, path)) as file:
        return (self.createResponse(HTTPCodes.OK.value, "".join(file.readlines()), "OK", headers))

  def processPost(self):
    pass

  def processOptions(self, headers):
    answer_body = ""
    with open(os.path.join(ROOT , "options.txt")) as optionsMethod:
      return (self.createResponse(HTTPCodes.OK.value, "".join(optionsMethod.readlines()), "OK", headers))

  def fileNotFound(self, headers):
    answer_body = ""
    with open(os.path.join(ROOT, FILE_NOT_FOUND)) as fileNot:
      return (self.createResponse(HTTPCodes.NOT_FOUND.value, "".join(fileNot.readlines()), "Not Found",
                                  headers))


  def createResponse(self, code, body, description, headers):
    answer_headers = headers["version"] + " " + str(code) + " " + description + "\n"
    answer_headers += "Server: Python socket HTTP Server\n"
    answer_headers += "Date" + time.ctime() + "\n"
    answer_headers += "Content-type: \n"
    answer_headers += "Content-length: \n"
    answer_headers += "Access-Control-Allow-Origin: localhost \n"
    answer_headers += "Access-Control-Allow-Methods: GET, POST, OPTIONS\n\n"
    #answer_headers = "{version} {status_code} {description} \n{headers}\n\n"\
    #  .format(version=headers["version"], status_code = code, headers = headers, description = description)
    answer_body = body
    answer = answer_headers + answer_body
    print(answer)
    answer = answer.encode()
    return answer