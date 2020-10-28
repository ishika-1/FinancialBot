from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow import logging
from logzero import logger
import pandas as pd
import numpy as np
import pickle
import logzero
from FinBot import helper
from FinBot import constants
from FinBot import trainer
from FinBot import functions
import os
import re

#trainer.train_intent_model()
#trainer.train_dialog_model()

logging.set_verbosity(logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def predict_intent(utterance):
	# import nlu settings

	min_confidence = constants.THRASHOLD

	max_length = 10
	glove_dimension = 100
	glove_path = constants.GLOVE_PATH
	verbose = constants.VERBOSE

	word_index, classes, embed_matrix = helper.get_token_data()

	tk = Tokenizer()

	tk.word_index = word_index

	temp = re.findall(r'\d+', utterance)
	numberlist = list(map(int, temp))

	amount = 0

	if (len(numberlist) == 1):
		amount = numberlist[0]
	if (len(numberlist) == 0):
		pass
	if (len(numberlist) > 1):
		for i in range(len(numberlist)):
			if (numberlist[i] <= 10):
				numberlist.pop(i)
		amount = numberlist[0]

	x_test = tk.texts_to_sequences([utterance])
	x_test = pad_sequences(x_test, maxlen=max_length, padding='post')

	# get trained model 
	# glove_dict = helper.generate_glove_dict(glove_path)
	vocab_size = len(tk.word_index) + 1

	# embed_matrix = helper.get_embedding_matrix(glove_dict, tk.word_index.items(), vocab_size, glove_dimension)
	model = helper.get_glove_model(vocab_size, glove_dimension, embed_matrix, max_length, len(classes))

	model = helper.load_nlp_model_weights(model)
	
	# predict 
	prediction = model.predict(x_test, verbose=verbose)

	predicted_class = helper.get_predicted_class(min_confidence, prediction, classes)

	return predicted_class, amount


def predict_action(domain_tokens, maxlen, num_features, sequence):
	try:
		class_predicted = None
		min_confidence = constants.THRASHOLD
		# prepare test data
		x_test = np.array(sequence)
		x_test = pad_sequences([x_test],  maxlen=maxlen, padding='post')

		# get model
		model = helper.create_dialog_network(maxlen, len(domain_tokens))

		# load weights
		model = helper.load_dm_model_weights(model)

		pred = model.predict(x_test, verbose=1)

		# get max score class
		max_score_index = np.argmax(pred)

		# log data predicted
		for key, val in domain_tokens.items():
			if val == max_score_index:
				class_predicted = key
				break

		return class_predicted, max_score_index
	except Exception as err:
		logger.error(err)
		raise err


def restart_predictor():
	helper.clear_prediction_data()
