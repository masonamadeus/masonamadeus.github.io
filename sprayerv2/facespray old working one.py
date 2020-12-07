from flask import Flask, request, Response
from flask_cors import CORS
import _thread
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, methods=['POST'])

SPRAY_Q = 0

@app.route('/', methods=['POST'])
def respond():
#    def spray():
#        GPIO.output(14, True);
#        time.sleep(3);
#        GPIO.output(14, False);
#        print('spray complete')
#        return
#    _thread.start_new_thread( spray, () )
    global SPRAY_Q
    SPRAY_Q += 1
    print('hit success');
    return Response(status=200)


def q_check():
    def sprayroutine():
        global SPRAY_Q
        sr = " Sprays Remaining"
 
        if SPRAY_Q > 0:
            GPIO.output(14, True)
            time.sleep(2)
            SPRAY_Q -= 1
            GPIO.output(14, False)
            print (str(SPRAY_Q) + sr)
            time.sleep(0.2)
 
        else:
            GPIO.output(14, False)
            
    while True:
        sprayroutine()
    
_thread.start_new_thread( q_check, () )



