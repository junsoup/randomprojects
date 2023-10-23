Notes:
I cannot for the life of me understand why the network is not performing well. I have a ton of data and tried like 50 different network architectures. The model seems to overfit despite cases with small network sizes.
I may have to revise my data format. This is likely the issue over a network being unable to learn since that is unlikely.
Revise network to be sequential. It was never able to learn that picked champions will be the same in the output for some reason. Assuming there is nothing wrong with my data, I could look into creating a sequential set up that considers one out "node" per output layer.

Files:

Data processing:
	champSequencer.py:
	for getting list of champion ids. the ids are not 0-n but rather just random numbers. Creates a one-to-one map of champion id's to 0-n ids

	DataCollector.py:
	my tool to farm games using riot APIs. They have a rate limit of like ~1.2 calls / second. I create a pseudo multi-thread setup (it's just one thread but it rotates through keys that are available per tick) for utilizing multiple keys.
	output format is winning 5 champion ids, 5 losing champ ids

	simulator.py:
	inputs output from DataCollector.py to "simulate" additional games by simulating other pick orders. At this point, the data is a massive file.
	
	pickai.py:
	inputs output from simulator.py to one-hot encode the data champion id. This is important since similar id values hold no meaning. transforms cvs, (plain ascii) to sparse tensors. This saves a lot of space.

Neural net:
	teampicker.py:
	inputs output from pickai.py. This is converted to a dataset and used to train a neural network. After training, the weights and biases are saved for future use. Uses GPU for cuda cores.
	
	predictor.py:
	loads in saved weights for user testing.

