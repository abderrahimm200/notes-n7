from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  #print("up")
  return "<h1>n7-notes</h1>"

def run():
  app.run(host = '0.0.0.0', port=8000)


def alive():
  t=Thread(target=run)
  t.start()
