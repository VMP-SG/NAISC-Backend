from flask import Flask, Response, request
from flask_cors import CORS
from threading import Thread
from API import *
from time import sleep
from modules.table_occupancy_check import *
from modules.queue_count import *

import cv2
app = Flask(__name__)
CORS(app)

# Define global variables
result = None
records = []
API = None  # Generator
API_active = False


@app.route("/")
def health_check():
  return "500 Internal Server Error"


@app.route("/startAPI")
def create_API_thread():

  def start_API():
    global API, API_active, result, records
    API_active = True
    API = run_API()
    while API_active:
      result = next(API)
      records.append(result)

  API_thread = Thread(target=start_API)
  API_thread.start()
  sleep(10)
  return "API started!"


@app.route("/stopAPI")
def stop_API_thread():  # Stops API but not the data stream. i.e. result variable is no longer updated
  global API_active
  API_active = False
  return "API stopped"

# @app.route("/test")
# def stream():
#   if request.headers.get('accept') == 'text/event-stream':
#     def events():
#       for i, c in enumerate(itertools.cycle('\|/-')):
#         yield "data: %s %d\n\n" % (c, i)
#         time.sleep(.1)  # an artificial delay
#     return Response(events(), content_type='text/event-stream')


def video_gen(camera_id, key):
  global result
  while True:
    ret, buffer = cv2.imencode('.jpg', result[camera_id][key])
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')  # concat frame one by one and show result


def data_gen(camera_id):
  global result
  while True:
    sleep(0.5)
    yield "data: %s\n\n" % (result[camera_id]["zone_people_count"])


def table_occupancy_gen():
  global records
  while True:
    sleep(0.5)
    # Uses the latest 10 records to determine table status
    yield "data: %s\n\n" % (str(is_table_occupied(records[-10:])))


def queue_count_gen():
  global result
  while True:
    sleep(0.5)
    yield "data: %s\n\n" % (str(queue_count(result)))


@app.route("/video/filter/<path:camera_id>")  # /video/A
def video_filter_feed(camera_id):
  if not API_active:
    return "No video feed as API is inactive"
  return Response(video_gen(camera_id, "labelled_frame"), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/video/raw/<path:camera_id>")
def video_raw_feed(camera_id):
  if not API_active:
    return "No video feed as API is inactive"
  return Response(video_gen(camera_id, "raw_frame"), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/count/zone/<path:camera_id>")  # /count/zone/A
def zone_stream(camera_id):
  if not API_active:
    return "No data feed as API is inactive"
  # TODO: uncomment this later
  # if request.headers.get('accept') == 'text/event-stream':
  return Response(data_gen(camera_id), content_type='text/event-stream')


@app.route("/tables")
def table_occupancy():
  if not API_active:
    return "No data feed as API is inactive"
  return Response(table_occupancy_gen(), content_type='text/event-stream')


@app.route("/queues")
def store_queue_count():
  if not API_active:
    return "No data feed as API is inactive"
  return Response(queue_count_gen(), content_type='text/event-stream')


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=3000)
