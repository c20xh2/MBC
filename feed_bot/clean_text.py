import os

count = 0
file_list = os.listdir('./text/')

for file in file_list:
	with open('text/{}'.format(file), 'r') as file:
		data = file.read()
		data = data.replace('\n', '').replace('  ', ' ')
	
	try:
		data = data.split('commentaire(s)')[0]
	except:
		pass

	phrase_list = data.split('.')

	for data in phrase_list:
		phrase = data.lstrip()
		if len(phrase) > 30:
			if 'dit:' not in phrase:
				if 'dit :' not in phrase:
					if '_' not in phrase:
						print('writting')
						with open('./text_clean/{}.txt'.format(count), 'w') as out:
							out.write('{}. \n'.format(phrase))
							count += 1
		else:
			print('skipping')