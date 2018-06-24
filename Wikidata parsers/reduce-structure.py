import time
import json
import argparse

supported_languages = None

def filterLanguages(property):
	selected = {}
	if supported_languages:
		for lang in supported_languages:
			if lang in property:
				selected[lang] = property[lang]
	else:
		selected = property
	return selected

def reduceLanguages(property):
	property = filterLanguages(property)
	for lang in property:
		if 'value' in property[lang]:
			property[lang] = property[lang]['value']
		else:
			list = []
			for item in property[lang]:
				list.append(item['value'])
			property[lang] = list
	return property

def reduceRelations(properties):
	relations = []
	for property in properties:
		#print('\tProperty:', property) #LOG
		for entity in properties[property]:
			if (entity['mainsnak']['datatype'] == 'wikibase-item'):
				if ('datavalue' in entity['mainsnak']):
					if (entity['mainsnak']['datavalue']['type'] == 'wikibase-entityid'):
						#print('\t\tEntity:', entity['id']) #LOG
						relation = {}
						relation['item'] = entity['mainsnak']['datavalue']['value']['id']
						relation['relation'] = property
						relation['rank'] = entity['rank']
						relations.append(relation)
	return relations

def parseItem(item):
	try:
		id = item['id']
		print('Item:', id) #LOG
		labels = reduceLanguages(item['labels'])
		if (len(labels) != 0):
			aliases = reduceLanguages(item['aliases'])
			descriptions = reduceLanguages(item['descriptions'])
			relations = reduceRelations(item['claims'])
			output = {'item':id, 'labels':labels, 'aliases':aliases, 'descriptions':descriptions, 'relations':relations}
		else:
			output = None
	except:
		output = None
	return output

def single_item(item):
	output_item = parseItem(item) if (item['type'] == 'item') else None
	return output_item

def big_item_list(input_file, output_file):
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
			output = single_item(json.loads(line))
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
	parser.add_argument('--languages', type=str, nargs='*')
	args = parser.parse_args()
	
	global supported_languages
	supported_languages = args.languages
	
	t0 = time.time()
	big_item_list(args.input_file, args.output_file)
	print(time.time()-t0, 'seconds')
	
	print("> Done")

if __name__ == "__main__":
	main()
