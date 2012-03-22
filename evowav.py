import random
import itertools
import numpy
import scipy.io.wavfile




def main():
	"""Read a wav file and shuffle the negative and positive pieces."""
	
	# Unpack sample wav file into a sample rate variable and numpy array
	samplerate, target_genotype = scipy.io.wavfile.read('target.wav')
		
	generation_size = 10
	population = []
	
	for i in range(0, generation_size):
		genotype = new_shuffled_genotype(target_genotype)
		fitness = get_fitness(genotype, target_genotype)		
		individual = {'genotype': genotype, 'fitness': fitness }
		population.append(individual)
	
	generation = 0
			
	while True:
		population.sort(key=lambda individual: individual['fitness'])
		
		if population[0]['fitness'] == 0:
			output = population[0]['genotype']
			scipy.io.wavfile.write('output.wav', 44100, output)
			break
		
		p1 = population[0]['genotype']
		p2 = population[1]['genotype']
		child_genotype = mate(p1, p2)
		child_fitness = get_fitness(child_genotype, target_genotype)
		if child_fitness < population[-1]['fitness']:
			population[-1] = {'genotype': child_genotype, 'fitness': child_fitness}
		
		mutated_genotype, mutantindex = mutate(population)
		mutated_fitness = get_fitness(mutated_genotype, target_genotype)
		population[mutantindex] = {'genotype': mutated_genotype, 'fitness': mutated_fitness}
		
	 	print generation, population[0]['fitness']
	 	
	 	if generation % 500 == 0:
	 		output = population[0]['genotype']
			scipy.io.wavfile.write('output.wav', 44100, output)
	 	
	 	generation += 1
	
	#output = new_shuffled_individual(target)
	#print get_fitness(output, target)
	#scipy.io.wavfile.write('output.wav', 44100, output)

def process_wav(wavdata):
	"""Read a wav file data array, detect zero crossings, split at zero crossings, and return a list of numpy arrays"""
	
	zerocrossings, = numpy.diff(numpy.sign(wavdata)).nonzero()
	zerocrossings += 1
	indices = [0] + zerocrossings.tolist() + [None]
	
	return [wavdata[i:j] for i, j in zip(indices[:-1], indices[1:])]

def shuffle_wav(partitions):
	"""Accept a list as input, separate into positive and negative chunks, shuffle, and return a shuffled nested list."""
	
	# Separate into positive and negative chunks
	poschunks = partitions[::2]
	negchunks = partitions[1::2]
	if poschunks[0][0] < 0:
		# Reverse the variable names if the first chunk isn't positive.
		negchunks, poschunks = poschunks, negchunks
	
	# Shuffle the lists
	random.shuffle(poschunks)
	random.shuffle(negchunks)
	
	# Zip the lists back together
	chunks = itertools.izip_longest(poschunks, negchunks, fillvalue=[])
	
	return numpy.hstack(item for sublist in chunks for item in sublist)

def get_fitness(individual_genotype, target_genotype):
	"""Compares sum of square differences between the two arrays."""
	return ((individual_genotype - target_genotype)**2).sum()

def new_shuffled_genotype(target_genotype):
	"""Creates a new shuffled individual from the target array. Returns a numpy array."""
	wavchunks = process_wav(target_genotype)
	return shuffle_wav(wavchunks).astype(numpy.int16)
	
def mate(parent1, parent2):
	spliceindex = random.randint(0, len(parent1)-1)
	return numpy.hstack((parent1[:spliceindex], parent2[spliceindex:]))

def mutate(population):
	i = random.randint(0, len(population)-1)
	mutation_target = population[i]
	mutation_genotype = mutation_target['genotype']
	processed_genotype = process_wav(mutation_genotype)
	j = random.randint(0, len(processed_genotype))
	k = random.randint(1, len(processed_genotype)-1)
	random.shuffle(mutation_genotype[j:k])
	shuffled_genotype = mutation_genotype
	return shuffled_genotype, i
			

main()
	