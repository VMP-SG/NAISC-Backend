from flask import Flask, Response, request
from flask_cors import CORS

import time
import itertools
import numpy as np
import cv2 as cv
app = Flask(__name__)
CORS(app)

@app.route("/")
def health_check():
  return "Health Check!"

@app.route("/hello")
def hello():
  return "Hello!"

@app.route("/test")
def stream():
  if request.headers.get('accept') == 'text/event-stream':
    def events():
      for i, c in enumerate(itertools.cycle('\|/-')):
        yield "data: %s %d\n\n" % (c, i)
        time.sleep(.1)  # an artificial delay
    return Response(events(), content_type='text/event-stream')

def video_gen():
  cap = cv.VideoCapture('videos/GoldenMile/GoldenMile_1.mp4')
  while True:
    success, frame = cap.read()  # read the camera frame
    if not success:
      cap.set(cv.CAP_PROP_POS_FRAMES, 0)
      continue
    else:
      ret, buffer = cv.imencode('.jpg', frame)
      frame = buffer.tobytes()
      yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route("/video")
def video_feed():
  return Response(video_gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)
