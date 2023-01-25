from flask import Flask, Response, request
from flask_cors import CORS

import time
import itertools
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

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=3000)
