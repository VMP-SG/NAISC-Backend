from flask import Flask, Response, abort, redirect, request
from flask_cors import CORS
from waitress import serve
from flask_swagger_ui import get_swaggerui_blueprint
from PIL import Image

from API import *
from threading import Thread
from time import sleep, time
from modules.table_occupancy_check import *
from modules.queue_count import *
from modules.table_people_count import *
import json
import copy
import base64
from io import BytesIO

import cv2
app = Flask(__name__)
CORS(app)

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Hawk-Eye Centre"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


# Define global variables
result = None
records = []
API = None  # Generator
API_active = False

@app.route("/")
def swagger():
  url = request.url
  return redirect(url + '/swagger')

@app.route("/startAPI")
def create_API_thread():

  def start_API():
    global API, API_active, result, records
    start_time = time()
    API_active = True
    API = run_API()
    while API_active:
      result = next(API)
      records.append(result)
      records = records[-10:]
      if time()-start_time > 600:  # 10 min idle timer
        API_active = False

  API_thread = Thread(target=start_API)
  API_thread.start()
  sleep(10)
  print("API started!")
  return "API started!"


@app.route("/stopAPI")
def stop_API_thread():  # Stops API but not the data stream. i.e. result variable is no longer updated
  global API_active
  API_active = False
  print("API stopped")
  return "API stopped"

def video_gen(camera_id, key):
  global result
  while True:
    ret, buffer = cv2.imencode('.jpg', result[camera_id][key])
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')  # concat frame one by one and show result

def count_gen():
  global result
  while True:
    sleep(0.5)
    yield "data: %s\n\n" % (json.dumps({key:result[key]["total_people_count"] for key in result}))

def zone_count_gen(camera_id):
  global result
  while True:
    sleep(0.5)
    yield "data: %s\n\n" % (result[camera_id]["zone_people_count"])


def table_occupancy_gen():
  global records
  while True:
    sleep(0.5)
    # Uses the latest 10 records to determine table status
    yield "data: %s\n\n" % (json.dumps(is_table_occupied(records)))

def tables_people_gen():
  global records
  while True:
    sleep(0.5)
    # Uses the latest 10 records to determine table count
    yield "data: %s\n\n" % (json.dumps(table_people_count(records)))

def table_people_gen(table_id):
  global records
  while True:
    sleep(0.5)
    yield "data: %s\n\n" % (table_people_count(records)[table_id])

def queues_count_gen():
  global result
  while True:
    sleep(0.5)
    yield "data: %s\n\n" % (json.dumps(queue_count(result)))

def queue_count_gen(stall_id):
  global result
  while True:
    sleep(0.5)
    yield "data: %s\n\n" % (queue_count(result)[stall_id])

def data_gen():
  global result
  if result:
    while True:
      response = copy.deepcopy(result)
      for key in response:
        labelled_img = Image.fromarray(response[key]["labelled_frame"])
        im_file = BytesIO()
        labelled_img.save(im_file, format="JPEG")
        labelled_bytes = im_file.getvalue()  # im_bytes: image in binary format.
        labelled_b64 = base64.b64encode(labelled_bytes).decode("UTF-8")

        raw_img = Image.fromarray(response[key]["labelled_frame"])
        raw_img.save(im_file, format="JPEG")
        raw_bytes = im_file.getvalue()  # im_bytes: image in binary format.
        raw_b64= base64.b64encode(raw_bytes).decode("UTF-8")

        response[key]['labelled_frame'] = labelled_b64
        response[key]['raw_frame'] = raw_b64
      yield "data: %s\n\n" % (json.dumps(response))

@app.route("/video/filter/<camera_id>")  # /video/A
def video_filter_feed(camera_id):
  if not API_active:
    abort(404)
  return Response(video_gen(camera_id, "labelled_frame"), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/video/raw/<camera_id>")
def video_raw_feed(camera_id):
  if not API_active:
    abort(404)
  return Response(video_gen(camera_id, "raw_frame"), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/count/zone/<camera_id>")  # /count/zone/A
def zone_stream(camera_id):
  if not API_active:
    abort(404)
  return Response(zone_count_gen(camera_id), content_type='text/event-stream')

@app.route("/count/zones")
def count_stream():
  if not API_active:
    abort(404)
  return Response(count_gen(), content_type='text/event-stream')

@app.route("/count/table/<int:table_id>")
def count_table_stream(table_id):
  if not API_active:
    abort(404)
  return Response(table_people_gen(table_id), content_type='text/event-stream')

@app.route("/count/tables")
def count_tables_stream():
  if not API_active:
    abort(404)
  return Response(tables_people_gen(), content_type='text/event-stream')

@app.route("/occupancy/tables")
def table_occupancy():
  if not API_active:
    abort(404)
  return Response(table_occupancy_gen(), content_type='text/event-stream')

@app.route("/count/queue/<int:stall_id>")
def store_queue_count(stall_id):
  if not API_active:
    abort(404)
  return Response(queue_count_gen(stall_id), content_type='text/event-stream')

@app.route("/count/queues")
def store_queues_count():
  if not API_active:
    abort(404)
  return Response(queues_count_gen(), content_type='text/event-stream')

@app.route("/api")
def data():
  if not API_active:
    abort(404)
  return Response(data_gen(), content_type='text/event-stream')

@app.errorhandler(404)
def error_handler(e):
  return "No data feed as API is inactive", 404

if __name__ == "__main__":
  serve(app, host='0.0.0.0', port=3000)
