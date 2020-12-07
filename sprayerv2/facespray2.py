from flask import Flask, request, Response, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from better_profanity import profanity
import _thread
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'secret!'
cors = CORS(app, methods=['POST'])
socketio = SocketIO(app)

if __name__ == "__main__":
    profanity.load_censor_words()

SPRAY_Q = 0

@app.route('/overlay')
def overlay():
    return render_template('overlay.html')

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
    req = request.get_json()
    value = req['value']
    censored_value = profanity.censor(value)
    socketio.emit('overlayNotif', {'value': censored_value})
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



