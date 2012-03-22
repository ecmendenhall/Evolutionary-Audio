# Import scipy audio tools, numpy, and randomization tools
import scipy
from scipy.io import wavfile

import numpy

from random import shuffle, randint

# Read a wav file data array, detect zero crossings, split at zero crossings, and return a nested list.
def process_wav(input):

	# Assign the wavefile data array to a variable.
	wavdata = input[1]

	# Detect zero crossings, i.e. changes in sign in the waveform data. The line below returns an array of the indices of elements after which a zero crossing occurs.
	zerocrossings = numpy.where(numpy.diff(numpy.sign(wavdata)))[0]
	# Increment each element in the array by one. Otherwise, the indices are off.
	zerocrossings = numpy.add(numpy.ones(zerocrossings.size, zerocrossings.dtype), zerocrossings)

	wavdatalist = wavdata.tolist()
	zerocrossingslist = zerocrossings.tolist()

	# Split the list at zero crossings. The function below splits a list at the given indices.		
	def partition(alist, indices):
		return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]

	return partition(wavdatalist, zerocrossingslist)
	

# Accept a list as input, separate into positive and negative chunks, shuffle, and return a shuffled nested list
def shuffle_wav(list):
	
	# Separate waveform chunks into positive and negative lists.
	positivechunks = []
	negativechunks = []

	for chunk in list:
		if chunk[0] < 0:
			negativechunks.append(chunk)
		elif chunk[0] > 0:
			positivechunks.append(chunk)
		elif chunk[0] == 0:
			positivechunks.append(chunk)
		
	# Shuffle the chunks and append them to a list, alternating positive with negative.
	shuffledchunks = []
	while len(positivechunks) >= 0 and len(negativechunks) > 0:
		currentpositivechunk = positivechunks.pop(randint(0, len(positivechunks)-1))
		shuffledchunks.append(currentpositivechunk)
		currentnegativechunk = negativechunks.pop(randint(0, len(negativechunks)-1))
		shuffledchunks.append(currentnegativechunk)

	return [chunk for sublist in shuffledchunks for chunk in sublist]

# Generate the 'fitness' of a given individual, defined as the sum of the squared difference between the individual and target array, i.e. a measurement of difference.	
def get_fitness(individual, target):
	return numpy.sum(numpy.subtract(individual, target)**2)
	
# Create a new shuffled individual from the target. Returns a numpy array.
def new_shuffled_individual(target):
	numpy.random.shuffle(target)
	flatchunks = [chunk for sublist in target for chunk in sublist]
	return numpy.array(flatchunks, dtype='int32')
	
def replicate(parent1, parent2):
	spliceindex = randint(0, len(parent1)-1)
	return parent1[:spliceindex] + parent2[spliceindex:]

# Read a sample wav file. The wavfile function returns a tuple of the file's sample rate and data as a numpy array, to be passed to the process_wav() function.
input = scipy.io.wavfile.read('sample.wav') 	
	
targetchunks = process_wav(input)
population = []

while len(population) < 20:
	population.append(new_shuffled_individual(targetchunks))

for individual in population:
	print get_fitness(individual, input[1])





#flatchunks = new_shuffled_individual(wavchunks)
#output = numpy.array(flatchunks, dtype='int32')
#print get_fitness(output, input[1])

#scipy.io.wavfile.write('output.wav', 44100, output)

def mutate_chunk(chunk):
	mutation = randint(0,1)
	if mutation == 0:
		chunk.reverse()
	else:
		for item in chunk:
			item = randint(-500, 500) + item
			
	return chunk