import upload
import webbrowser
from threading import Timer

# def open_browser():
#       webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
	# webbrowser.open('http://127.0.0.1:5000/')
	upload.app.run(debug = True)