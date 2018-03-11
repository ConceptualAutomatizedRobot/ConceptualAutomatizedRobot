from flask import Flask, render_template, Response
from camera import VideoCamera
from threading import Thread
import time

frame = b''
camera = VideoCamera()

def function():
	global frame
	global camera
	while True:
		frame = camera.get_frame()

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

def gen():
	global frame
	while True:
		# frame = camera.get_frame()
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
	return Response(gen(),
					mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	t = Thread(target=function)
	t.start()
	app.run(host='0.0.0.0', threaded=True)

# from flask import Flask, render_template, Response
# from camera import VideoCamera

# app = Flask(__name__)

# @app.route('/')
# def index():
# 	return render_template('index.html')

# def gen(camera):
# 	while True:
# 		frame = camera.get_frame()
# 		yield (b'--frame\r\n'
# 			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# @app.route('/video_feed')
# def video_feed():
# 	return Response(gen(VideoCamera()),
# 					mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == '__main__':
# 	print("0")
# 	app.run(host='0.0.0.0', debug=True, threaded=True)
# 	print("1")