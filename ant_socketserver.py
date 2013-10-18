#! /usr/bin/env python3
# View open sockets: netstat -tulnap
import asyncore, os, threading, time
host=''
port=2004

class EchoKill():
    def __init__(self, port):
        print("Killking sockets")
        # kill any currently open sockets
        try:
            pid = os.popen("netstat -tulnap 2>/dev/null | grep "+str(port)+" | awk {'print $7'} | awk -F/ {'print $1'}").read()
            os.popen("kill -9 "+pid+" 2>/dev/null")
        except Exception as e:
            print("All old sockets cleaned")


class EchoHandler(asyncore.dispatcher_with_send):
    data = 0

    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.send(data)
            data = str(data.decode("utf-8")).strip()
            EchoHandler.data = data
            print ('Recieved command "'+data+'"')

    def saved_data(self):
       newdata = EchoHandler.data
       EchoHandler.data = 0
       return newdata

class EchoServer(asyncore.dispatcher):
    handler = 0

    def __init__(self, host, port):
        EchoKill(port)
        print("Listening on port "+str(port))
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        print('Incoming connection from %s' % repr(addr))
        EchoServer.handler = EchoHandler(sock)
    
    def new_data(self):
        if EchoServer.handler==0:
          return 0
        return EchoServer.handler.saved_data() 

server = EchoServer(host, port)
loop_thread = threading.Thread(target=asyncore.loop, name="Asyncore Loop")
loop_thread.start()
while True:
	print (server.new_data())
	time.sleep(1)





