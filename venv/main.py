import sys
from MyHTTPServer import MyHTTPServer

if __name__ == '__main__':
  host = sys.argv[1]
  port = int(sys.argv[2])

  server = MyHTTPServer(host, port)
  try:
    server.serveForever()
  except KeyboardInterrupt:
    pass