# keep_alive.py
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def keep_alive():
    Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8080}).start()
