import os

count = 0
file_list = os.listdir('./text/')

for file in file_list:
	with open('text/0.txt', 'r') as file:
		data = file.read()
		data = data.replace('\n', '')
	
	phrase_list = data.split('.')

	for data in phrase_list:
		phrase = data.lstrip()
		with open('./text_clean/{}.txt'.format(count), 'w') as out:
			out.write(phrase)
			count += 1