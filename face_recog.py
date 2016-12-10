import gpios
import gsm_read_sms
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import os

button = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(button,GPIO.IN)
GPIO.setwarnings(False)

RESIZE_FACTOR = 4
scaleFactor = 1.1
minNeighbors = 1
minSize = (30,30)
flags = cv2.cv.CV_HAAR_SCALE_IMAGE




gpios.power_on()
gsm_read_sms.sms_init()

class OpenCVRecog:
    
    def __init__(self):
        self.DEBUG_IMAGE = "captured_debug.png"
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        self.face_dir = 'negatives'
        self.unknown_face = 'unknown'
        self.path = os.path.join(self.face_dir, self.unknown_face)
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        self.model = cv2.createEigenFaceRecognizer()
        self.names = []
    
    def load_trained_data(self):
        print "Loading trained images..."
        names = {}
        key = 0
        for(subdirs,dirs,files) in os.walk('face_data'):
            for subdir in dirs:
                names[key] = subdir
                key +=1
        self.names = names
        self.model.load('eigen_trained_data.xml')
        return
        
    def read(self):
        
        while 1:
            message = gsm_read_sms.read_sms()
            print message
            
            if(GPIO.input(button)):
                print 'pressed button...'
                data = gpios.camera()
                image = cv2.imdecode(data,1)
                inImg = np.array(image)
                outImg = self.process_image(inImg)
                cv2.imwrite(self.DEBUG_IMAGE,image)
                
            elif message == "GO":
                gpios.GREEN_ON()
                time.sleep(2)
                gpios.GREEN_OFF()
                
                
            else:
                print 'button is not pressed...'
                gpios.RED_OFF()
                gpios.GREEN_OFF()
                gpios.YELLOW_OFF()
            
        return
    def process_image(self,inImg):
        print "Processing image..."
        frame = cv2.flip(inImg,1)
        resized_width, resized_height = (112,92)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_resized = cv2.resize(gray, (gray.shape[1]/RESIZE_FACTOR,gray.shape[0]/RESIZE_FACTOR))
        faces = self.face_cascade.detectMultiScale(
            gray_resized,
            scaleFactor = scaleFactor,
            minNeighbors = minNeighbors,
            minSize = minSize,
            flags = flags)
        
        if len(faces)>0:
            print "Face detected...."
            gpios.RED_OFF()
        
            for i in range(len(faces)):
                face_i = faces[i]
                x = face_i[0] * RESIZE_FACTOR
                y = face_i[1] * RESIZE_FACTOR
                w = face_i[2] * RESIZE_FACTOR
                h = face_i[3] * RESIZE_FACTOR
                face = gray[y:y+h, x:x+w]
                face_resized = cv2.resize(face,(resized_width,resized_height))
                confidence = self.model.predict(face_resized)
                print str(confidence)
                if confidence[1]<300:
                    person = self.names[confidence[0]]
                    print "FACE REGISTERED"
                    print "PERSON NAME: "+person
                    gpios.GREEN_ON()
                    gpios.YELLOW_OFF()
                    time.sleep(1.5)
                    
                    
                else:
                    print "NOT REGISTERED"
                    gpios.YELLOW_ON()
                    gpios.GREEN_OFF()
                    img_no = sorted([int(fn[:fn.find('.')])for fn in os.listdir(self.path) if fn[0]!='.']+[0])[-1]+1
                    cv2.imwrite('%s/%s.png' % (self.path,img_no),frame)
                    PATH_IMG = "/home/pi/DP_FACE_RECOG_REVAMPED/negatives/unknown/"+str(img_no)+'.png'
                    PATH_IMG = gsm_read_sms.send_mms(PATH_IMG)
                    
        else:
            print "No face detected..."
            gpios.RED_ON()
            
        return frame
        
if __name__ == '__main__':
    face_recog = OpenCVRecog()
    face_recog.load_trained_data()
    face_recog.read()
    
       
