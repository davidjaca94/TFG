import os
import time
import json
import argparse

def recover(item):
	item_path = 'items\\' + item + '.json'
	if os.path.exists(item_path):
		ficheroentrada = open(item_path, 'r').read()
		return json.loads(ficheroentrada)
	else:
		return None

def replace(relations, lang):
	output = []
	for relation in relations:
		item = recover(relation)
		if item:
			if (lang in item['labels']):
				output.append(item['labels'][lang])
	return output

def parse_lang(item, lang):
	if (lang in item['labels']):
		relations = replace(item['relations'], lang)
		if (len(relations) > 0):
			output = {item['labels'][lang]: relations}
			return output
		else:
			return None
	else:
		return None

def parse(item):
	if (len(item['relations']) > 0):
		output_es = parse_lang(item, 'es')
		output_en = parse_lang(item, 'en')
		return [output_es, output_en]
	else:
		return [None, None]

def process(input_file, output_file):
	# Es preciso que el json este formado como una entrada por linea
	ficheroentrada = open(input_file, 'r')
	ficherosalida_es = open(output_file.replace(".json", "_es.json"), "w+")
	ficherosalida_en = open(output_file.replace(".json", "_en.json"), "w+")

	count_es = 0
	count_en = 0
	for line in ficheroentrada:
		line = line.replace('\n','').replace('\r','')
		if (line == '['):
			ficherosalida_es.write('{\n')
			ficherosalida_en.write('{\n')
		elif (line == ']'):
			ficherosalida_es.write('\n}')
			ficherosalida_en.write('\n}')
		else:
			if (line[-1] == ','): line = line[:-1]
			output_es, output_en = parse(json.loads(line))
			if output_es:
				count_es += 1
				head = ',\n' if (count_es > 1) else ''
				ficherosalida_es.write(head + json.dumps(output_es)[1:-1])
			if output_en:
				count_en += 1
				head = ',\n' if (count_en > 1) else ''
				ficherosalida_en.write(head + json.dumps(output_en)[1:-1])
			if (output_es or output_en): print('ES: %d, EN: %d' % (count_es, count_en)) #LOG

	ficheroentrada.close()
	ficherosalida_es.close()
	ficherosalida_en.close()

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
