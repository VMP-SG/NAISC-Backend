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
  if not cap.isOpened():
    print("Cannot open camera")
    exit()
  while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    cv.namedWindow("window", cv.WND_PROP_FULLSCREEN)
    cv.setWindowProperty("window",cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
    # if frame is read correctly ret is True
    if ret:
        cv.imshow("window", frame)
    else:
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        continue
    # Our operations on the frame come here
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    # cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
      break
  # releasing the capture
  cap.release()
  cv.destroyAllWindows()
  
@app.route("/video")
def video_feed():
  return Response(video_gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)
