import requests
from urllib2 import URLError, HTTPError
from HTMLParser import HTMLParser

#from xml.etree import cElementTree as etree

class Downloader():
	'''
	Class to retrieve HTML code from a specific page
	'''

	def __init__(self,url):
		self.url = url
		self.contents = ''
#		self.tb = etree.TreeBuilder()

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

class Tag:
	'''
	Class for Tag
	'''

	name = '';
	text = '';
	first_child = 0
	parent = 0
	next_sibling = 0
	closed = 0
	depth = 0
	attrs = [];
	isRecipe = 0

	def __eq__(self, other):
		for attr in ['name', 'text', 'first_child', 'parent', 'next_sibling', 'closed', 'depth', 'attrs', 'isRecipe']: 
			v1, v2 = [getattr(obj, attr, _NOTFOUND) for obj in [self,other]]
			if v1 is _NOTFOUND or v2 is __NOTFOUND:
				return False
			elif v1 != v2:
				return False
		return True

	def get_tag_info_str(self):
		c ,p ,s = 'none', 'none', 'none'
		if self.first_child != 0:
			c = self.first_child.name
		if self.parent != 0:
			p = self.parent.name
		if self.next_sibling != 0:
			s = self.next_sibling.name

		for name, value in self.attrs:
			if name == 'class' and value == 'listing recipe hrecipe ' :
				self.isRecipe = 1
				break

		formatString = u" Name = {}, Text = {} \n Parent = {}, First Child = {}, Next Sibling = {} \n Closed = {}, Depth = {} \n isRecipe = {} \n\n\n".format(self.name, self.text, p, c, s, self.closed, self.depth, self.isRecipe)
		return formatString

class EatYourBooksParser(HTMLParser):
	'''
	Class for parsing page from EatYourBooks.com for a given cuisine.
	Inherits from HTMLParser
	'''
	
	tag_list = []
	depth = 0
	previous_tag = 'none'
	mode = 'nonsilent'

	def handle_starttag(self, tag, attrs):			
		self.depth = self.depth + 1
		t = Tag()
		t.name = tag
		t.depth = self.depth
		t.attrs = attrs
		if self.previous_tag == 'start':
			t.parent = self.tag_list[len(self.tag_list)-1]
			self.tag_list[len(self.tag_list)-1].first_child = t
		elif self.previous_tag == 'end':
			for x in reversed(self.tag_list):
				if x.depth == self.depth:
					x.next_sibling = t
					if t.parent == 0:
						t.parent = x.parent
					break
		elif self.previous_tag == 'startend': 
			t.parent = self.tag_list[len(self.tag_list)-1].parent
			self.tag_list[len(self.tag_list)-1].next_sibling = t

		self.tag_list.append(t)
		self.previous_tag = 'start'
	
	def handle_endtag(self, tag):
		for x in reversed(self.tag_list):
			if x.name == tag and x.closed == 0:
				x.closed = 1
				break
		self.depth = self.depth - 1
		self.previous_tag = 'end'
	
	def handle_startendtag(self, tag, attrs):
		t = Tag()
		self.depth = self.depth + 1
		t.name = tag
		t.depth = self.depth 
		t.closed = 1
		
		if self.previous_tag == 'start' :
			t.parent = self.tag_list[len(self.tag_list)-1]
			self.tag_list[len(self.tag_list)-1].first_child = t
		elif self.previous_tag == 'startend':
			t.parent = self.tag_list[len(self.tag_list)-1].parent
			self.tag_list[len(self.tag_list)-1].next_sibling = t
		elif self.previous_tag == 'end':
			for x in reversed(self.tag_list):
				if x.depth == self.depth:
					x.next_sibling = t
					if t.parent == 0:
						t.parent = x.parent
					break
		self.tag_list.append(t)
		self.depth = self.depth - 1
		self.previous_tag = 'startend'

	def handle_data(self, data):
		self.depth = self.depth + 1
		
		for x in reversed(self.tag_list):
			if x.depth == self.depth - 1:
				x.text = (x.text + ' ' + data.strip(' \n\t')).strip(' \n\t')
				break
		self.depth = self.depth - 1
	
	def print_tag_list(self, u):
		f = open('tag_list.txt', 'w')
		for l in self.tag_list:
			f.write(l.get_tag_info_str().encode('UTF-8'))
		f.close()

	def clear_tag_list(self):
		self.tag_list.__delslice__(0, len(self.tag_list))

	def pretty_print_tags(self):
		for t in self.tag_list:
			s = ''
			s = s + self.get_ident_str(t.depth-1)
			s = s + self.get_tag_str(t.name)

	def get_ident_str(self, n):
		s = ''
		while( n != 0 ):
			s =  s + '     '
			n = n -1
		return s
	
	def get_tag_str(self, name):
		return '<{}>'.format(name)

	def find_first_tag(self, name):
		r = 0
		for t in self.tag_list:
			if t.name == name:
				r = t
				break
		return r

	def print_first_tag_info(self, name):
		t = self.find_first_tag(name)
		if t == 0:
			print ('Tag: {} not found'.format(name))
		else:
			print t.get_tag_info_str()


class EatYourBooksRecipe():
	id = 0
	root_depth = 0
	is_indexed = 0
	categories = []
	ingredients = []
	class BookData():
		shelf_status = ""
		recipe_str = ""
		recipe_url = ""
		source_str = ""
		source_url = ""
		author_str = ""
		author_url = ""
	class Feedback():
		rating = 0
		notes_str = ""
		notes_url = ""
		online_url = ""

	
	def __init__(self, tag_list, start_index):
		root_depth = start_index
		recursive_parser(tag_list, start_index)

	def recursive_parser(self, tag_list, start_index):
		node = tag_list[start_index]
		child = tag_list[start_index + 1]
		if node.depth > child.depth + 1:
			return start_index + 1
		if node.child == child and child.parent == node: 
			switch (node.depth-root_depth):
			
			
				
			

	
if __name__ == '__main__':
	url = "http://www.eatyourbooks.com/recipes/indian"
	eatYourBooksParser = EatYourBooksParser()
	downloader = Downloader(url)
	downloader.download()
	eatYourBooksParser.feed(downloader.contents.decode('UTF-8'))
	eatYourBooksParser.print_tag_list(1);
	#tag list is created as an array. 
	#eatYourBooksParser.extract_recipe()
	

	
