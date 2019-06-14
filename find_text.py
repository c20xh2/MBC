import requests
from bs4 import BeautifulSoup

PAGE_COUNT = 1
PAGE_MAX = 113



def trouve_des_links_de_vidange(PAGE_COUNT):
	url = 'https://www.journaldemontreal.com/auteur/mathieu-bock-cote/page/{}'.format(PAGE_COUNT)
	r = requests.get(url)
	soup = BeautifulSoup(r.text,'html')
	print(soup.text)




while PAGE_COUNT <= PAGE_MAX:
	trouve_des_links_de_vidange(PAGE_COUNT)
	PAGE_COUNT += 1
