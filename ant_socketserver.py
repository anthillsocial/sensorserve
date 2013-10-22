#! /usr/bin/env python3
import asyncore, os, threading, time
# TODO: Remove EchoKill - its very bad & was implemented because reuse address wasn't working!!
# To use these classes:
#   server = EchoServer('', 2004)
#   while True:
#     print (server.new_data())
#     time.sleep(1)

class EchoKill():
    def __init__(self, port):
        print(cols.OKGREEN+"Network: Closed all old open sockets"+cols.E)
        # kill any currently open sockets
        try:
            os.popen("netstat -tulnap 2>/dev/null | grep "+str(port)+" | awk {'print $7'} | awk -F/ {'print $1'} | xargs -I {} kill -9 {}").read()
            #os.popen("kill -9 "+pid+" 2>/dev/null")
        except Exception as e:
            print(cols.OKGREEN+"Network: All old sockets cleared"+cols.E)


class EchoHandler(asyncore.dispatcher_with_send):
    data = -1

    def handle_read(self):
        data = self.recv(8192)
        if data:
            # self.send(data) echo test
            data = str(data.decode("utf-8")).strip()
            EchoHandler.data = data
            print (cols.OKGREEN+'\nNetwork: Recieved command "'+data+'"'+cols.E)

    def saved_data(self):
       newdata = EchoHandler.data
       EchoHandler.data = -1
       return newdata

class EchoServer(asyncore.dispatcher):
    handler = False

    def __init__(self, host, port):
        # make sure old open ports are killed
        EchoKill(port)
        print(cols.OKGREEN+"Network: Listening on port "+str(port)+cols.E)
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        # Now run this server in a nonblocking thread
        loop_thread = threading.Thread(target=asyncore.loop, name="Asyncore Loop")
        loop_thread.start()

    def handle_accepted(self, sock, addr):
        print(cols.OKGREEN+'\nNetwork: Incoming connection from %s' % repr(addr)+cols.E)
        EchoServer.handler = EchoHandler(sock)
    
    def new_data(self):
        if EchoServer.handler==False:
          return -1
        return EchoServer.handler.saved_data() 
    
    def senddata(self, newstr):
        self.handler.send(bytes(newstr, 'UTF-8'))

class cols:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    E = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
