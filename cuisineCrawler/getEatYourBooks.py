import requests
from urllib2 import URLError, HTTPError
from HTMLParser import HTMLParser


class Downloader():
	'''
	Class to retrieve HTML code from a specific page
	'''

	def __init__(self,url):
		self.url = url
		self.contents = ''

	def download(self):
		try: 
			r = requests.get(self.url)
						
		except HTTPError as e:
			print('The server couldn\'t fulfill the request.')
			print('Error code: ', e.code)
		except URLError as e:
			if hasattr(e, 'reason'):
				print('Failed to reach server. ')
				print('Reason: ', e.reason)
			elif hasattr(e, 'code'):
				print('Server couldn\'t fullfill the request.')
				print('Error code: ', e.code)
		else:
			contents = r.text
			contents = contents.encode(r.encoding)
			self.contents = contents
			f = open('urlcontents.txt', 'w')
			f.write(self.contents)
			
class EatYourBooksParser(HTMLParser):
	'''
	Class for parsing page from EatYourBooks.com for a given cuisine.
	Inherits from HTMLParser
	'''

	def handle_starttag(self, tag, attrs):
		for name, value in attrs: 
			if name == 'class' and value == 'listing recipe hrecipe ' :
				k=1
	
	def handle_endtag(self, tag):
		i=1
	
	def handle_data(self, data):
		j=1

if __name__ == '__main__':
	url = "http://www.eatyourbooks.com/recipes/indian"
	eatYourBooksParser = EatYourBooksParser()
	downloader = Downloader(url)
	downloader.download()
	eatYourBooksParser.feed(downloader.contents.decode('UTF-8'))
	
