#! /usr/bin/env python3
import serial, time, os, re, sys
from ant_socketserver import *

port = '/dev/ttyACM2'
connected = 0
counter = 0
dotcount = 0
# Server host, port (set host to '127.0.0.1' for lovcal connections only)
server = EchoServer('', 2005)

while True:
	if connected == 1:
		try:
			# Check the network for any commands
			networkmsg = server.new_data()
			if networkmsg!=-1:
				print(cols.OKGREEN+"\nNetwork: Action="+networkmsg+cols.E)
			# Read data being sent by the ardunio
			content = ser.readline()
			content = content.decode("utf-8").strip()
			msg  = "";
			if content == 'A':
				msg = "Ready & waiting for instruction..."
				ser.write(bytes("1", 'UTF-8'))
			else:
			    ser.write(bytes("1", 'UTF-8'))
			    #time.sleep(0.5)
			# Print ou the response
			sys.stdout.write("\r\x1b[KArduino: Recieved \""+content+"\". Polled #"+str(counter)+' times. '+msg)
			sys.stdout.flush()
			counter += 1
		except Exception as e:
			print("\nArduino: Lost connection with error: "+str(e))
			connected = 0
	else:
		## Check USB connection is up
		usb = os.popen("lsusb | grep Arduino | awk '{print $7}'").read()
		usb = usb.strip()
		## Grab the port	
		port = os.popen("ls /sys/class/tty/tty* | grep ACM | tail -1 | awk -F/ '{print $5}' | rev | cut -c 2- | rev").read()
		port = port.strip()
		port = '/dev/'+port
		# Now try and open a serial connection
		try:
			ser = serial.Serial(port, 9600, timeout=1)
			print ('\nArduino: Connected via port "'+port+'"')
			connected = 1;
		except Exception as e:
			if usb!="Arduino":
				if dotcount >=4:
					dotcount = 1
				else:
					dotcount += 1;
				dots = "."*dotcount
				sys.stdout.write("\r\x1b[K Arduino"+"No USB device found. Searching"+dots)
			else:
				print("\nArduino: Plugged in but no communication via port: "+port)
			connected = 0 
			


# Man help content
"""
// ---------------------------------------------------------
// Arduino Code that works with the python above example
// Slightly developed from the basic communication examples
// ---------------------------------------------------------
int firstSensor = 0;    // first analog sensor
int secondSensor = 0;   // second analog sensor
int thirdSensor = 0;    // digital sensor
int inByte = 0;         // incoming serial byte

void setup()
{
  // start serial port at 9600 bps and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }

  
  pinMode(2, INPUT);   // digital sensor is on digital pin 2
  establishContact();  // send a byte to establish contact until receiver responds 
}

void loop()
{
  // if we get a valid byte, read analog ins:
  if (Serial.available() > 0) {
    // get incoming byte:
    inByte = Serial.read();
    // read first analog input:
    firstSensor = analogRead(A0);
    // read second analog input:
    secondSensor = analogRead(A1);
    // read  switch, map it to 0 or 255L
    thirdSensor = map(digitalRead(2), 0, 1, 0, 255);  
    // send sensor values:
    Serial.print(firstSensor);
    Serial.print(",");
    Serial.print(secondSensor);
    Serial.print(",");
    Serial.println(thirdSensor);               
  }
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.println("A");   // send an initial string
    delay(300);
  }
}
"""


