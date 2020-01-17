import pickle
import cv2 as cv
import numpy as np
from flask import Flask, request
from flask_restful import Resource, Api
from os.path import join, dirname, realpath

MODEL_PATH = join(dirname(realpath(__file__)), '../model')

app = Flask(__name__)

api = Api(app)

data = []

class ImageClassificationAPI(Resource):
	def tresholding(image, kind='original'):
		img = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
		if kind == 'original':
			return img
		elif kind == 'global':
			ret, img = cv.threshold(img,127,255,cv.THRESH_BINARY)
			return img
		elif kind == 'mean':
			return cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY,11,2)
		elif kind == 'gaussian':
			return cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
		else:
			return False

	def reshape(image):
		img = cv.resize(image, (500, 500))
		return img.reshape(-1)

	def predict_model(image, probability = False):
		img = reshape(tresholding(image, 'original'))
		model = pickle.load(open(join(MODEL_PATH, 'logistic_model_original.sav'), 'rb'))
		prediction = model.predict(img)
		
		output = {}

		output['file'] = image['file_name']
		if probability:
			result = {}
			probability = model.predict_proba(img).reshape(-1)
			for class_name, prob in zip(class_dir_list, list(probability)):
				result[class_name] = prob
			output['result'] = result

		output['class'] = prediction[0]
		return output

	def get(self, image):
		for x in data:
			if x['file'] == image:
				return x
		return {'file':None}

	def post(self):
		image = request.files['image']
		img = cv.cvtColor(cv.imread(image), cv.COLOR_BGR2RGB)
		output = predict_model(img)
		data.append(output)
		return output

	def delete(self):
		for index, x in enumerate(data):
			if x['data'] == image:
				tem = data.pop(index)
				return {'note' : 'Deleted'}

api.add_resource(ImageClassificationAPI, '/result/<string:image>')