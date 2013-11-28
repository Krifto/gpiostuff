from flask import Flask, render_template
import datetime
import socket

app = Flask(__name__)


@app.route("/")
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'HELLO!',
      'time': timeString
      }
   return render_template('main.html', **templateData)

@app.route("/setColor/<color>")
def readPin(color):
   try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect(("localhost", 8080))
      s.send(color)
      s.send("\n")
      response = "Color " + color + " set."
   except Exception as e:
      response = "There was an error setting color " + color + ": " + str(e) + "."

   templateData = {
      'title' : 'Status of RGB' + color,
      'response' : response
      }

   return render_template('ledstrip.html', **templateData)


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
