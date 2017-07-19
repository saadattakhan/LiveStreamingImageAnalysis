from flask import Flask, render_template, url_for, request, redirect, flash, Response
from datetime import datetime
import cStringIO as StringIO
from PIL import Image, ImageFont, ImageDraw
import urllib2
import numpy as np
import dlib
import io

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

def gen():
	print("inside gen");
	try:
		host = "10.15.0.125:8080/video"
		hoststr = 'http://' + host

		stream=urllib2.urlopen(hoststr)
		print("streaming started");

		bytes=''

		while True:
			bytes+=stream.read(1024)
			a = bytes.find('\xff\xd8')
			b = bytes.find('\xff\xd9')
			if a!=-1 and b!=-1:
				print("jpeg found");
				jpg = bytes[a:b+2]
				bytes= bytes[b+2:]
				streamline = StringIO.StringIO(jpg)
				img = Image.open(streamline)


				frame=np.array(img)					
				
				convjpg = Image.fromarray(frame)
				imgByteArr=io.BytesIO()
				convjpg.save(imgByteArr,format="jpeg")
				imgByteArr=imgByteArr.getvalue()	
				yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + imgByteArr + b'\r\n')
	except Exception as e:
		print(e)

@app.route('/livestream')
def livestream():
	return Response(gen(),
		mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
	app.run(debug=True)
