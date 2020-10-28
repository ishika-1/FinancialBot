import os
from os.path import join, dirname
import numpy as np
import json
import pickle
import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras import Sequential, layers
import yaml
import requests
#import expenseTrackerFunctions
import logzero
from logzero import logger
#from app.main.ai 
from FinBot import constants

NLU_MODEL_PATH = join(dirname(__file__), 'models', 'nlu', constants.CPD_WL_1_PATH)
DIALOG_MODEL_PATH = join(dirname(__file__), 'models', 'dialog', constants.CPD_DM_1_PATH)
TOKENIZER_DATA_PATH = join(dirname(__file__), 'data', constants.TOKENIZER_PATH)
UTTERANCE_PATH = join(dirname(__file__), 'data', constants.UTTERANCE_PATH)
DIALOG_OPTIONS_PATH = join(dirname(__file__), 'data', constants.DIALOG_OPTIONS_PATH)
DIALOG_STATE_PATH = join(dirname(__file__), 'data', constants.DIALOG_STATE_PATH)
DIALOG_PATH = join(dirname(__file__), 'data', constants.DIALOG_PATH)
CREDS_PATH = join(dirname(__file__), 'creds', constants.CREDS_PATH)
DOMAIN_PATH = join(dirname(__file__), constants.DOMAIN_PATH)
CASUAL_RESPONSE = join(dirname(__file__), '../answer_templates', constants.CASUAL_RESPONSE)
START_RESPONSE = join(dirname(__file__), '../answer_templates', constants.START_RESPONSE)
STOP_RESPONSE = join(dirname(__file__), '../answer_templates', constants.STOP_RESPONSE)


def create_dialog_network(time_steps, classes_num):
	vocab_size = 60
	vec_size = 20
	model = Sequential()
	model.add(layers.Embedding(vocab_size, vec_size, input_length=time_steps))
	model.add(layers.LSTM(vec_size, dropout=0.2, recurrent_dropout=0.2))
	model.add(layers.Dense(classes_num, activation='softmax'))

	return model


def get_glove_model(vocab_size, glove_dimension, embed_matrix, max_length, num_classes):
	keras.backend.clear_session()
	model = Sequential()
	embed = layers.Embedding(vocab_size, glove_dimension, weights=[embed_matrix], input_length=max_length,
							 trainable=False)

	model.add(embed)
	model.add(layers.Flatten())
	model.add(layers.Dense(30, activation=tf.nn.relu)),
	model.add(layers.Dropout(0.5))
	model.add(layers.Dense(num_classes, activation=tf.nn.softmax))

	return model


def save_model(model):
	try:
		model.save(NLU_MODEL_PATH)
	except Exception as err:
		raise err


def save_dialog_model(model):
	try:
		model.save(DIALOG_MODEL_PATH)
	except Exception as err:
		raise err


def load_nlp_model_weights(model):
	try:
		model.load_weights(NLU_MODEL_PATH)
		return model
	except Exception as err:
		raise err


def load_dm_model_weights(model):
	try:
		model.load_weights(DIALOG_MODEL_PATH)
		return model
	except Exception as err:
		raise err


def get_embedding_matrix(glove_dict, token_items, vocab_size, vector_dim):
	marix = np.zeros((vocab_size, vector_dim))

	for word, idx in token_items:
		vector = glove_dict.get(word)
		if vector is not None:
			marix[idx] = vector

	return marix


def generate_glove_dict(path):
	
	glove_index = dict()
	gl_path = join(dirname(__file__) + '/data/', path)

	file = open(gl_path, encoding="utf8")

	for line in file:
		splited_line = line.split()
		word = splited_line[0]
		coeficient = np.array(splited_line[1:], dtype='float32')

		glove_index[word] = coeficient

	file.close()

	return glove_index


def get_training_data_from_json(path):
	train_data = []
	classes = []

	training_data = json.loads(open(path).read())

	for batch in training_data['intents']:
		for pattern in batch['patterns']:
			train_data.append([pattern, batch['tag']])

		# generate  unique classes array
		if batch['tag'] not in classes:
			classes.append(batch['tag'])

	return train_data, classes


def convert_y_data_to_labels(data, classes):
	for set in data:
		set[1] = classes.index(set[1])
	return data


def save_tokenizer_data(word_index, classes, embed_matrix):
	try:
		pickle.dump({'word_index': word_index, 'classes': classes, 'embed_matrix': embed_matrix},
					open(TOKENIZER_DATA_PATH, 'wb'))
	except Exception as err:
		raise err


def get_token_data():
	data = pickle.load(open(TOKENIZER_DATA_PATH, 'rb'))
	word_index = data['word_index']
	classes = data['classes']
	embed_matrix = data['embed_matrix']

	return word_index, classes, embed_matrix


def get_predicted_class(threshold, scores, classes):
	prediction = scores[0]
	pred_class = None

	max_score_index = np.argmax(prediction)
	score = prediction[max_score_index]

	# filter trough threshold
	if threshold < score:
		pred_class = classes[max_score_index]
	else:
		logger.info('Prediction is lower than threshold')

	print('\n')
	print("Predicted score: {sc}, Index: {idx}, Class: {cls}".format(
		sc=score,
		idx=max_score_index,
		cls=pred_class
	))
	print("\n\n")

	return pred_class


def get_domain_data():
	document = open(DOMAIN_PATH, 'r')
	parsed = yaml.load(document)

	return parsed


def get_creds_data():
	document = open(CREDS_PATH, 'r')
	parsed = yaml.load(document)

	return parsed


def get_dialog_flow_data():
	document = open(DIALOG_PATH, 'r')
	dialog = yaml.load(document)

	return dialog


def save_dialog_options(domain_tokens, num_features, sample_length):
	"""set serialized  object - dialog data from file"""

	try:
		pickle.dump({'domain_tokens': domain_tokens,
					 'sample_length': sample_length,
					 'num_features': num_features},
					open(DIALOG_OPTIONS_PATH, 'wb'))
	except Exception as err:
		raise err


def get_dialog_options():
	try:

		"""get serialized  object - dialog data from file"""
		data = pickle.load(open(DIALOG_OPTIONS_PATH, 'rb'))
		domain_tokens = data['domain_tokens']
		maxlen = data['sample_length']
		num_features = data['num_features']

		return domain_tokens, maxlen, num_features
	except Exception as err:
		raise err


def get_closes_value(values, value):
	min_val = min(values, key=lambda x: abs(x - value))
	return min_val


def get_dialog_state():
	try:
		data = pickle.load(open(DIALOG_STATE_PATH, 'rb'))

		return data
	except Exception as err:
		logger.info('Dialog state file not found')
		return None


def save_dialog_state(data):
	"""set serialized  object - dialog state from file"""

	try:
		pickle.dump(data, open(DIALOG_STATE_PATH, 'wb'))
	except Exception as err:
		raise err


def get_utterance(domain_tokens, action_predicted):
	try:
		utter_data = json.loads(open(UTTERANCE_PATH).read())
		utterances = utter_data['utterances']
		token = None

		for key, value in domain_tokens.items():
			if value == action_predicted:
				token = key
				break

		return utterances[token]
	except KeyError as err:
		logger.error(err)
		return 'Crap!!!! So weird thing happened on my side. Please wait a bit I need report it to our devs'


def generate_utter(template):
	utter_data = json.loads(open(UTTERANCE_PATH).read())
	utterances = utter_data['utterances']

	return utterances[template]


def check_key_exists(obj, key):
	if key in obj:
		return True

	return False


def post_slack_message(text, channel_id):
	url = 'https://slack.com/api/chat.postMessage'
	cred = get_creds_data()

	msg = {
		'token': cred['slack']['slack_token'],
		'channel': channel_id,
		'text': text
	}

	r = requests.post(url, data=msg)
	print('Slack postMessage code: ', r.status_code)


def clear_prediction_data():
	try:
		os.remove(DIALOG_STATE_PATH)
	except FileNotFoundError as err:
		logger.info('{} was already removed.'.format(DIALOG_STATE_PATH))


def generate_ga_answer_template(data={}, action_type=None):
	if action_type == constants.NEW:
		res = json.loads(open(START_RESPONSE).read())
	elif action_type == constants.ACTIVE:
		text = {
			"text_to_speech": data['text']
		}
		res = json.loads(open(CASUAL_RESPONSE).read())
		res['expected_inputs'][0]['input_prompt']['initial_prompts'] = [text]
	else:
		res = json.loads(open(STOP_RESPONSE).read())

	return res
