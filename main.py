from flask import Flask
app = Flask(__name__)

@app.route("/")
def health_check():
  return "Health Check!"

if __name__ == "__main__":
  app.run(port=8080)
