import serial
import RPi.GPIO as GPIO
import os, time
import pyimgur

#GPIO.setmode(GPIO.BOARD)

# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

myList = [1,2]
CLIENT_ID = "35e99a18a53c221"

def sms_init():
    port.write('AT'+'\r\n')
    rcv = port.read(10)
    print rcv


    port.write('ATE0'+'\r\n')# Disable the Echo
    rcv = port.read(10)
    print rcv


    port.write('AT+CMGF=1'+'\r\n')# Select Message format as Text mode 
    rcv = port.read(10)
    print rcv


    port.write('AT+CMGL="ALL"'+'\r\n')# Select Message format as Text mode 
    rcv = port.read(10)
    print rcv

def read_sms():
    port.write('AT+CMGL="REC UNREAD"'+'\r')# Select Message format as Text mode 
    rcv = port.readall()
    msg = rcv.split('\r\n')
    print rcv
    print msg
    myList = [str(e) for e in msg]
    print len(myList)
    message = myList[2]
    return message

def send_mms(PATH_IMG):
    print PATH_IMG
    
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH_IMG, title ="Uploaded Intruder!")
    print (uploaded_image.title)
    MSG = uploaded_image.link

    port.write('AT+CMGF=1'+'\r\n')# Select Message format as Text mode 
    rcv = port.read(10)
    print rcv
    time.sleep(0.5)

    port.write('AT+CNMI=2,1,0,0,0'+'\r\n') # New SMS Message Indications
    rcv = port.read(10)
    print rcv
    time.sleep(0.5)

    # Sending a message to a particular Number

    port.write('AT+CMGS="9175488573"'+'\r\n')
    rcv = port.read(10)
    print rcv
    time.sleep(0.5)

    port.write( MSG +'\r\n')# Message
    rcv = port.read(10)
    print rcv

    port.write("\nSomeone is trying to steal your ride..."+'\r\n')# Message
    rcv = port.read(10)
    print rcv

    port.write("\x1A") # Enable to send SMS
    for i in range(10):
	rcv = port.read(10)
	print rcv
    

    
    



