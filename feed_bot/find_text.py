import requests
from bs4 import BeautifulSoup



def trouve_des_links_de_vidange():
	
	vidange_list = []
	PAGE_COUNT = 0
	PAGE_MAX = 113

	while PAGE_COUNT <= PAGE_MAX:

		PAGE_COUNT += 1
		
		url = 'https://www.journaldemontreal.com/auteur/mathieu-bock-cote/page/{}'.format(PAGE_COUNT)
		print('[{}/{}] Finding links'.format(PAGE_COUNT, PAGE_MAX))
		r = requests.get(url)
		soup = BeautifulSoup(r.text,'html.parser')

		link_list = soup.find('div', {'class', 'ajaxList'})

		for link in link_list.findAll('a'):
			href = link.get('href')
			vidange_list.append(href)

	return vidange_list

def extract_vidange(url):

	r = requests.get(url)
	soup = BeautifulSoup(r.text,'html.parser')
	
	for div in soup.find_all('div', {'class':'embedded-others'}):
		div.decompose()
	for div in soup.find_all('div', {'class' : 'post-body'}):
		div.decompose()

	try:
		vidange = soup.find('div', {'class' : 'article-main-txt'})	
		return vidange.text
	except:
		return None

def save_vidange(vidange, count, url):
	filename = './text/{}.txt'.format(count)

	with open(filename, 'w') as out:
		# out.write('{}\n'.format(url))
		out.write(vidange)

count = 0

vidange_list = trouve_des_links_de_vidange()
total = len(vidange_list)
for url in vidange_list:

	print('[{}/{}] Working on {}'.format(count, total, url))
	vidange = extract_vidange(url)
	if vidange != None:
		save_vidange(vidange, count, url)
		count +=1 
	else:
		print('[!!!] {}'.format(url))