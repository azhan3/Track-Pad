from flask import Flask, render_template, Response
from werkzeug.middleware.profiler import ProfilerMiddleware
import cv2
import sys
import src.Backend as Backend

feed = Backend.MainWindow(cv2.VideoCapture(0))

app = Flask(__name__, static_folder='static')


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