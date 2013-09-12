from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import re
from html.parser import HTMLParser


class Downloader():
	'''
	Class to retrieve HTML code from a specific page
	'''

	def __init__(self,url):
		self.url = url
		self.contents = ''

	def download(self):
		req = Request(self.url)
		try: response = urlopen(req)
		except HTTPError as e:
			print('The server couldn\'t fulfill the request.')
			print('Error code: ', e.code)
		except urllib.error.URLError as e:
			if hasattr(e, 'reason'):
				print('Failed to reach server. ')
				print('Reason: ', e.reason)
			elif hasattr(e, 'code'):
				print('Server couldn\'t fullfill the request.')
				print('Error code: ', e.code)
		else:
			contents = response.read()
			self.contents = contents.decode(encoding='UTF-8')
			f = open('urlContents.txt','w')
			f.write(self.contents)
			

class EatYourBooksParser(HTMLParser):
	'''
	Class for parsing page from EatYourBooks.com for a given cuisine.
	Inherits from HTMLParser
	'''

	def handle_starttag(self, tag, attrs):
		if tag.find('li',0,tag.__len__()-1) >= 0:
			print ('Encountered a start tag: ', tag)
	
	def handle_endtag(self, tag):
		if tag.find('li',0,tag.__len__()-1) >= 0:
			print ('Encountered an end tag: ', tag)
	
	def handle_data(self, data):
		if data.find('li',0,data.__len__()-1) >= 0:
			print ('Encountered some data: ', data)


if __name__== '__main__':
	url="http://www.eatyourbooks.com/recipes/indian"
	eatYourBooksParser = EatYourBooksParser()
	downloader = Downloader(url)
	downloader.download()
	eatYourBooksParser.feed(downloader.contents)
	
