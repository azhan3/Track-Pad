from flask import Flask, render_template, Response, request, jsonify
import cv2
import sys
import json
import time
import src.Backend as Backend
import threading
import requests


feed = None
app = Flask(__name__, static_folder='static')


def init_backend(callback):
    global feed
    feed = Backend.MainWindow(cv2.VideoCapture(0))
    callback(feed)


def start_backend(callback):
    threading.Thread(target=init_backend, args=(callback,)).start()


def start_feed():
    """Start the video feed"""
    def callback(feed):
        app.feed = feed
        app.run_threaded = True

    start_backend(callback)


start_feed()


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


stop_flag = False


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag"""
    if not hasattr(app, 'run_threaded'):
        image_binary = open("./static/Assets/loading_icon.gif", "rb").read()
        return Response(image_binary, mimetype='image/gif')
    else:
        global stop_flag; stop_flag = True

        response = Response(
            app.feed.run(), mimetype='multipart/x-mixed-replace; boundary=frame')
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response


def check_run_threaded(stop_flag):
    while not stop_flag:
        print("CHECK", file=sys.stderr)
        if hasattr(app, 'run_threaded'):
            # Do something here, for example start the video feed
            print("FOUND", file=sys.stderr)
            url = 'http://localhost:46832/reload'
            requests.get(url)

            break

        time.sleep(1)  # Wait for 1 second before checking again

# Start the function in a separate thread

threading.Thread(target=check_run_threaded, args=(stop_flag,)).start()


@app.route("/update_gesture", methods=["POST"])
def update_gesture():
    # parse the JSON request body
    gestures = request.json.get("gestures")

    # update the gesture assignment in the config.json file
    with open('./src/config.json', 'r') as file:
        config_p = json.load(file)

    config_p['gestures'] = gestures

    tmp = []
    for i in gestures:
        feed.MouseDict[i] = feed.actions[gestures[i]]
        if (gestures[i] == "Swipe"):
            tmp.append(i)
        print(i, gestures[i])
    config.SwipeList = tmp

    with open('./src/config.json', 'w') as file:
        json.dump(config_p, file)

    # return a success response to the client
    return {"success": True}


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=16969)
