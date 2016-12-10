#GPIO PINS
#LEDS
#RED = GPIO 16
#YELLOW = GPIO 20
#GREEN = GPIO 21
#LIGHT GREEN = GPIO 26
#SWITCH = GPIO 23

import RPi.GPIO as GPIO
import time
import picamera
import io
import numpy as np
 


ledRed = 16
ledYellow = 20
ledGreen = 21
ledLightGreen = 26

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ledRed,GPIO.OUT)
GPIO.setup(ledYellow,GPIO.OUT)
GPIO.setup(ledGreen,GPIO.OUT)
GPIO.setup(ledLightGreen,GPIO.OUT)

def power_on():
    GPIO.output(ledRed,GPIO.HIGH)
    GPIO.output(ledYellow,GPIO.HIGH)
    GPIO.output(ledGreen,GPIO.HIGH)
    GPIO.output(ledLightGreen,GPIO.HIGH)

    time.sleep(1.5)

    GPIO.output(ledRed,GPIO.LOW)
    GPIO.output(ledYellow,GPIO.LOW)
    GPIO.output(ledGreen,GPIO.LOW)
    GPIO.output(ledLightGreen,GPIO.LOW)
    

def RED_ON():
    GPIO.output(ledRed,GPIO.HIGH)
def RED_OFF():
    GPIO.output(ledRed,GPIO.LOW)


def YELLOW_ON():
    GPIO.output(ledYellow,GPIO.HIGH)
def YELLOW_OFF():
    GPIO.output(ledYellow,GPIO.LOW)

def GREEN_ON():
    GPIO.output(ledGreen,GPIO.HIGH)
def GREEN_OFF():
    GPIO.output(ledGreen,GPIO.LOW)


def LIGHTGREEN_ON():
    GPIO.output(ledLightGreen,GPIO.HIGH)
def LIGHTGREEN_OFF():
    GPIO.output(ledLightGreen,GPIO.LOW)

def camera():
    print 'opening camera....'
    data = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.capture(data, format='jpeg')
    data = np.fromstring(data.getvalue(),dtype=np.uint8)
    return data
    
    
    

    
    
    







