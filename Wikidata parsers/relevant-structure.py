import time
import json
import argparse

def relevant(relations):
	output = []
	
	for relation in relations:
		if (relation['rank'] == "preferred"):
			output.append(relation['item'])
	
	return output

def parse(item):
	output = {}
	output['item'] = item['item']
	output['labels'] = item['labels']
	output['aliases'] = item['aliases']
	output['relations'] = relevant(item['relations'])
	#output = output if (len(output['relations']) > 0) else None
	return output

def process(input_file, output_file):
	# Es preciso que el json este formado como una entrada por linea
	ficheroentrada = open(input_file,'r')
	ficherosalida = open(output_file,"w+")

	count = 0
	for line in ficheroentrada:
		line = line.replace('\n','').replace('\r','')
		if (line == '['):
			ficherosalida.write('[\n')
		elif (line == ']'):
			ficherosalida.write('\n]')
		else:
			if (line[-1] == ','): line = line[:-1]
			output = parse(json.loads(line))
			if output:
				count += 1
				print('line', count) #LOG
				head = ',\n' if (count > 1) else ''
				ficherosalida.write(head + json.dumps(output))

	ficheroentrada.close()
	ficherosalida.close()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--input_file', type=str, required=True)
	parser.add_argument('--output_file', type=str, required=True)
	args = parser.parse_args()

	t0 = time.time()
	process(args.input_file, args.output_file)
	print(time.time()-t0, 'seconds')
	
	print("> Done")

if __name__ == "__main__":
	main()
