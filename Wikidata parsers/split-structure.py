import os
import time
import json
import ijson
import argparse
from multiprocessing.pool import Pool

JOBS = 100000
THEADS = 100

def save(item):
	file = 'items\\' + item['item'] + '.json'
	path = os.path.dirname(file)
	if path: os.makedirs(path, exist_ok=True)
	
	if not os.path.exists(file):
		ficherosalida = open(file, "w+")
		ficherosalida.write(json.dumps(item))
		ficherosalida.close()

def process(input):
	ficheroentrada = open(input, 'r')

	count = 0
	buffer = []
	items = ijson.items(ficheroentrada, 'item')
	for item in items:
		buffer.append(item)
		if (len(buffer) == JOBS):
			t0 = time.time()
			with Pool(THEADS) as p:
				p.map(save, buffer)
			buffer = []
			count += JOBS
			seconds = time.time()-t0
			print("+%s = %d in %f seconds" % (JOBS, count, seconds)) #LOG

	ficheroentrada.close()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--input_file', type=str, required=True)
	args = parser.parse_args()

	t0 = time.time()
	process(args.input_file)
	print(time.time()-t0, 'seconds')
	
	print("> Done")

if __name__ == "__main__":
	main()
