import os, threading
from bottle import Bottle, static_file, route, template

class BottleServer:
    def __init__(self, host, port, rootdir, debug=False):
        self._host = host
        self._debug = debug
        self._rootdir = rootdir
        self._port = port
        self._killoldports()
        self._app = Bottle()
        self._route()        

    def _route(self):
        self._app.route('/', method="GET", callback=self._index)
        self._app.route('/<name>', callback=self._index)
        self._app.route('/static/<filename:path>', callback=self._static)

    def start(self):
        self._app.run(host=self._host, port=self._port, debug=self._debug)

    def loop(self):
        loop_thread = threading.Thread(target=self.start)
        loop_thread.start()

    def _static(self, filename=""):
        return static_file(filename, self._rootdir) 

    def _index(self, name=""):
        # return template('Hello {{name}}, how are you?', name=name)
        body = template('body.tpl');
        return template('index.tpl', name=name, body=body)

    def _killoldports(self):
        try:
           os.popen("netstat -tulnap 2>/dev/null | grep "+str(self._port)+" | awk {'print $7'} | awk -F/ {'print $1'} | xargs -I {} kill -9 {}").read()
        except Exception as e:
           print('')
           #print(cols.OKGREEN+NS+"All old sockets cleared"+cols.E)

# Tom run it normally
#  httpserver = BottleServer(host='', port=2005, rootdir='/path/to/static/files')
#  httpserver.start(); # start normally

# Or start in a non blocking thread
#httpserver = BottleServer(host='', port=2005, rootdir='/path/to/static/files')
#httpserver.loop() 
#while 1:
#  i=1
   
