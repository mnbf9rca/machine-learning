def runTests():
	import numpy as np
	import pandas as pd
	import matplotlib.pyplot as plt
	data_path = 'Bike-Sharing-Dataset/hour.csv'

	rides = pd.read_csv(data_path)
	rides[:24*10].plot(x='dteday', y='cnt')
	dummy_fields = ['season', 'weathersit', 'mnth', 'hr', 'weekday']
	for each in dummy_fields:
	    dummies = pd.get_dummies(rides[each], prefix=each, drop_first=False)
	    rides = pd.concat([rides, dummies], axis=1)

	fields_to_drop = ['instant', 'dteday', 'season', 'weathersit', 
	                  'weekday', 'atemp', 'mnth', 'workingday', 'hr']

	data = rides.drop(fields_to_drop, axis=1)
	quant_features = ['casual', 'registered', 'cnt', 'temp', 'hum', 'windspeed']
	# Store scalings in a dictionary so we can convert back later
	scaled_features = {}
	for each in quant_features:
	    mean, std = data[each].mean(), data[each].std()
	    scaled_features[each] = [mean, std]
	    data.loc[:, each] = (data[each] - mean)/std

	# Save data for approximately the last 21 days 
	test_data = data[-21*24:]

	# Now remove the test data from the data set 
	data = data[:-21*24]

	# Separate the data into features and targets
	target_fields = ['cnt', 'casual', 'registered']
	features, targets = data.drop(target_fields, axis=1), data[target_fields]
	test_features, test_targets = test_data.drop(target_fields, axis=1), test_data[target_fields]
	# Hold out the last 60 days or so of the remaining data as a validation set
	train_features, train_targets = features[:-60*24], targets[:-60*24]
	val_features, val_targets = features[-60*24:], targets[-60*24:]
	from my_answers import NeuralNetwork
	def MSE(y, Y):
	    return np.mean((y-Y)**2)

	inputs = np.array([[0.5, -0.2, 0.1]])
	targets = np.array([[0.4]])
	test_w_i_h = np.array([[0.1, -0.2],
	                       [0.4, 0.5],
	                       [-0.3, 0.2]])

	test_w_h_o = np.array([[0.3],
	                       [-0.1]])

	network = NeuralNetwork(3, 2, 1, 0.5)
	network.weights_input_to_hidden = test_w_i_h.copy()
	network.weights_hidden_to_output = test_w_h_o.copy()


	network.train(inputs, targets)

	network = NeuralNetwork(3, 2, 1, 0.5)
	network.weights_input_to_hidden = test_w_i_h.copy()
	network.weights_hidden_to_output = test_w_h_o.copy()


	network.run(inputs)