from os.path import join, dirname
import numpy as np
import tensorflow as tf

from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.preprocessing.text import Tokenizer

from logzero import logger
#from app.main.ai 
from FinBot import helper

#from app.main.ai 
from FinBot import constants


def train_intent_model():
	logger.info('Start intent model training --------->>>>>>>>>')
	max_length = 10
	glove_dimension = 100
	epochs = 400

	try:
		glove_path = constants.GLOVE_PATH
		verbose = constants.VERBOSE
		intents_path = join(dirname(__file__), 'data', constants.INTENTS_PATH)
		#print(glove_path)

		glove_dict = helper.generate_glove_dict(glove_path)
		training_data, classes = helper.get_training_data_from_json(intents_path)

		# generate labels from training data
		training_data = helper.convert_y_data_to_labels(training_data, classes)

		# convert to numpy array
		training_data = np.array(training_data)
		labels = training_data[:, 1]
		utterances = training_data[:, 0]

		# prepare tokenizer
		tk = Tokenizer()
		tk.fit_on_texts(utterances)
		vocab_size = len(tk.word_index) + 1

		# integer encode utterances
		encoded_utterances = tk.texts_to_sequences(utterances)
		print(encoded_utterances)
		padded_utterances = pad_sequences(encoded_utterances, maxlen=max_length, padding='post')
		print(padded_utterances)

		embed_matrix = helper.get_embedding_matrix(glove_dict, tk.word_index.items(), vocab_size, glove_dimension)

		model = helper.get_glove_model(vocab_size, glove_dimension, embed_matrix, max_length, len(classes))

		model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

		model.summary()

		# train the model
		print('x_train: ', padded_utterances)
		print('labels:', labels)
		model.fit(padded_utterances, labels, epochs=epochs, verbose=verbose)

		# save model weights
		helper.save_model(model)

		# save tokenizer data
		helper.save_tokenizer_data(tk.word_index, classes, embed_matrix)

		print('================>>>>>>>>>>>>>>>>NLU TRAINING DONE<<<<<<<<<<<<<<<<<=============')

	except Exception as err:
		raise err

def generate_sequences_and_labels(sequence):
	x, y = [], []
	max_length = len(sequence) - 1

	for idx, action in enumerate(sequence):
		x_sample, y_sample = [], []
		# stop when last sample treated
		if idx == max_length:
			break

		if action.startswith(constants.INTENT_TEMPLATE):
			x_sample = sequence[: idx + 1]

			x.append(x_sample)
			y.append(sequence[idx + 1])

	return x, y


def tokenize_matrix(data, tokens):
	for idx, sample in enumerate(data):
		data[idx] = list(map(lambda sq: tokens[sq], sample))
	return data


def train_dialog_model():
	logger.info('Start train dialog model ----------->>>>>>>>')
	domain_tokens = dict()
	x_train = []
	y_train = []
	max_length = 1
	num_features = 1
	num_epochs = 500

	try:
		domain_data = helper.get_domain_data()

		for idx, action in enumerate(domain_data['actions_list']):
			# create dict where with action name prop and index as a value (start with 1)
			domain_tokens[action] = (idx + 1)
		dialog_data = helper.get_dialog_flow_data()

		# get X, Y from sequence
		for flow in dialog_data['dialogs']:
			sequence = flow['flow']

			splitted_seq, labels = generate_sequences_and_labels(sequence)

			# get max dialog length
			if len(sequence) > max_length:
				max_length = len(sequence)

			x_train = x_train + splitted_seq
			y_train = y_train + labels

		# Tokenize training set
		x_train = tokenize_matrix(x_train, tokens=domain_tokens)

		# get first element from list because of smaller dimension
		y_train = tokenize_matrix([y_train], tokens=domain_tokens)[0]

		# pad sequences
		x_train = pad_sequences(x_train, maxlen=max_length - 1, padding='post')

		# one hot encode Y
		y_train = tf.one_hot(y_train, len(domain_tokens))

		# get LSTM model 
		model = helper.create_dialog_network(max_length - 1, len(domain_tokens))
		model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

		model.summary()

		print('------------- x_train ---------------')
		print(x_train)
		print(domain_tokens)

		# fit model
		model.fit(x_train, y_train, epochs=num_epochs, verbose=1, steps_per_epoch=2)

		# save model
		helper.save_dialog_model(model)

		# save dialog tokens
		helper.save_dialog_options(domain_tokens, num_features, sample_length=max_length - 1)

		print('================>>>>>>>>>>>>>>>>DIALOG TRAINING DONE<<<<<<<<<<<<<<<<<=============')

	except Exception as err:
		raise err
