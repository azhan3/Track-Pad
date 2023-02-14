from flask import Flask, render_template, Response, request, jsonify
from werkzeug.middleware.profiler import ProfilerMiddleware
import cv2
import sys
import json
import time
import src.Backend as Backend

#feed = Backend.MainWindow(cv2.VideoCapture(0))

app = Flask(__name__, static_folder='static')

@app.route("/update-checkstate", methods=["POST"])
def update_checkstate():
    check_state = request.json.get("checkState")
    with open('./src/config.json', 'r') as file:
        config_p = json.load(file)

    config_p['control']['pause'] = check_state

    with open('./src/config.json', 'w') as file:
        json.dump(config_p, file)
    return {"status": "success"}

@app.route("/config.json")
def config():
    with open("./src/config.json", "r") as file:
        config = json.load(file)
        return jsonify(config)


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(feed.run(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run()