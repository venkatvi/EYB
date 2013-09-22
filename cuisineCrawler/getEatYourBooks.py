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
	list_index = 0

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

		t.list_index = len(self.tag_list)
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
		t.list_index = len(self.tag_list)
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
	'''
	Class parses out recipe snippets from HTML
	Typical recipe snippet is:
	<li class="listing recipe hrecipe ">
           <div class="book-img">
              <a class="gallery" data-recipe-link="/library/recipes/1140785/tamarind-fish-curry" href="http://c3327103.r3.cf0.rackcdn.com/tamarind-fish-curry-1140785l1.jpg" title="Tamarind fish curry"><img alt="Tamarind fish curry" src="http://c3327103.r3.cf0.rackcdn.com/tamarind-fish-curry-1140785m1.jpg"></img></a>
           </div>
	   <div class="book-data">
	     <div class="bookshelf-status"></div>
	     <div class="book-title">
	        <h2 class="title fn"> 
                    <a href="/library/recipes/1140785/tamarind-fish-curry">Tamarind fish curry</a>
                </h2>
		<h3>
                    <i>&nbsp;from&nbsp;</i>
                    <a class="title" href="/library/89732/serious-eats">Serious Eats</a>
	       </h3>
	   </div>        
           <ul class="feedback">
                <li class="rating">
                    <span class='stars' rating='0' entityType='Recipe' entityId='1140785' title='Click on a star to rate'><a class="star star-left-off" value="0.5"></a><a class="star star-right-off" value="1"></a><a class="star star-left-off" value="1.5"></a><a class="star star-right-off" value="2"></a><a class="star star-left-off" value="2.5"></a><a class="star star-right-off" value="3"></a><a class="star star-left-off" value="3.5"></a><a class="star star-right-off" value="4"></a><a class="star star-left-off" value="4.5"></a><a class="star star-right-off" value="5"></a></span></li>
                <li class="notes" title="View notes for this recipe"><a class="title" href="/library/recipes/1140785/tamarind-fish-curry#notes" title="">0</a>
		</li>
                <li class="online">
                     <a class="view-online" href="http://www.seriouseats.com/recipes/2013/09/tamarind-fish-curry-recipe.html" title="View complete recipe on 3rd party website" target="_blank">Recipe Online</a>
                 </li>
            </ul>
            <ul class="meta">
                <li>
                    <b>Categories:</b> Curry; Quick / easy; Main course; Cooking for 1 or 2; Indian
                </li>
                <li>
                    <b>Ingredients:</b> turmeric; curry leaves; fennel seeds; tamarind; rice flour; kingfish fillets; chilli powder; ground coriander; ground cumin
                </li>
                <li>
                </li>
            </ul>
	  </div>
	  <div class="clear"></div>
	</li>
	'''
	id = 0
	type = ""
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
	
	
	def __init__(self, tag_list, start_index, end_index):
		child_nodes=filter(lambda x: x.depth == tag_list[start_index].depth + 1, tag_list[start_index: end_index -1])
		if len(child_nodes) == 2:
			parse_book_data(tag_list, child_nodes[1].list_index, end_index)

	def parse_book_data(self, tag_list, start_index, end_index):
		child_nodes = filter(lambda x: x.depth == tag_list[start_index].depth + 1, tag_list[start_index: end_index-1])
		if len(child_nodes) == 4: # bookshelf_status, book_title, feedback, meta.
			parse_bookshelf_status(tag_list, child_nodes[0].list_index, child_nodes[1].list_index)
			parse_book_title(tag_list, child_nodes[1].list_index, child_nodes[2].list_index)
			parse_feedback(tag_list, child_nodes[2]. list_index, child_nodes[3].list_index)
			parse_rating(tag_list, child_nodes[3].list_index, end_index)

	def parse_bookshelf_data(self, tag_list, start_index, end_index):
		child_nodes = filter(lambda x: x.depth == tag_list[start_index].depth + 1, tag_list[start_index: end_index - 1])
		#how to handle? 

	def parse_book_title(self, tag_list, start_index, end_index):
		child_nodes = filter(lambda x: x.depth == tag_list[start_index].depth + 1, tag_list[start_index:end_index -1])
		if len(child_nodes) == 2:
			parse_title_fn(tag_list, child_nodes[0].list_index, child_nodes[1].list_index)
			parse_from_by(tag_list, child_nodes[1].list_index, end_index)
				  
	def parse_feedback(self, tag_list, start_index, end_index):
		child_nodes = filter(lambda x: x.depth == tag_list[start_index].depth + 1, tag_list[start_index:end_index - 1])
		if len(child_nodes) == 3:
			parse_rating(tag_list, child_nodes[0].list_index, child_nodes[1].list_index)
			parse_notes(tag_list, child_nodes[1].list_index, child_nodes[2].list_index)
			parse_online(tag_list, child_nodes[2].list_index, end_index)

	def parse_meta(self, tag_list, start_index, end_index):
		child_nodes = filter(lambda x: x.depth == tag_list[start_index].depth + 1, tag_list[start_index:end_index - 1])
		if len(child_nodes) == 3:
			parse_categories(tag_list, child_ndoes[0].list_index, child_nodes[1].list_index)
			parse_ingredients(tag_list, child_nodes[1].list_index, child_nodes[2].list_index)
			parse_index_status(tag_list, child_nodes[2].list_index, end_index)

	def parse_title_fn(self, tag_list, start_index, end_index):
		child_node = tag_list[start_index + 1]
		#ahref node as child_node. 
		if child_node.name == 'a':
			for attr in child_node.attr:
				if attr.name == 'href': 
					self.BookData().recipe_url = attr.value
			self.BookData().recipe_str = child_node.text

	def parse_from_by(self, tag_list, start_index, end_index):
		child_nodes = filter(lambda x: x.name == 'i', tag_list[start_index:end_index - 1])
		for child_node in child_nodes:
			fromby_text = child_node.text
			fromby_text = fromby_text.strip()
			fromby_text = fromby_text.strip('&nbsp;')
			
			grand_child_node = tag_list[child_node.list_index + 1]
			for attr in grand_child_node.attr:
				if grand_child_node.name == 'span' and attr.name == 'class' and attr.value == 'title':
			       		self.BookData().source_str = grand_child_node.text
				if grand_child_node.name == 'a' and attr.name == 'class' and attr.value == 'author':
					self.BookData().author_str = grand_child_node.text
				if grand_child_node.name == 'a' and attr.name == 'href':
					self.BookData().author_url = attr.value
			       
	def parse_categories(self, tag_list, start_index, end_index):
		child_node = tag_list[start_index +1]
		if child_node.text == 'Categories:':
			categories_text = tag_list[start_index].text
			categories_text = categories_text.strip()
			self.categories = categories_text.split(';')
			self.categories = map(lambda s: s.strip(), self.categories)
	
	def parse_ingredients(self, tag_list, start_index, end_index):
		child_node = tag_list[start_index + 1]
		if child_node.text == 'Ingredients:':
			ingred_text = tag_list[start_index].text
			ingred_text = ingred_text.strip()
			self.ingredients = ingred_text.split(';')
			self.ingredients = map(lambda s: s.strip(), self.ingredients)
			
	def parse_index_status(self, tag_list, start_index, end_index):
		child_node = tag_list[start_index + 1]
		if child_node.name == 'b' and child_node.text == 'Member Indexed': 
			self.is_indexed = 1
		
	def parse_rating(self, tag_list, start_index, end_index):
		child_node = tag_list[start_index + 1]
		if child_node.name == 'span':
			for attr in child_node.attr:
				if attr.name == 'rating':
					self.Feedback().rating = int(attr.value)
				if attr.name == 'entitytype':
					self.type = attr.value
				if attr.name == 'entityid':
					self.id = int(attr.value)
	def parse_notes(self, tag_list, start_index, end_index):
		child_node = tag_list[start_index + 1]
		if child_node.name == 'a':
			for attr in child_node.attr:
				if attr.name == 'href':
					self.Feedback().notes_url = attr.value
	def parse_online(self, tag_list, start_index, end_index):
		child_node = tag_list[start_index + 1]
		if child_node.name == 'a':
			for attr in child_node.attr:
				if attr.name == 'href':
					self.Feedback().online_url = attr.value
	
	
if __name__ == '__main__':
	url = "http://www.eatyourbooks.com/recipes/indian"
	eatYourBooksParser = EatYourBooksParser()
	downloader = Downloader(url)
	downloader.download()
	eatYourBooksParser.feed(downloader.contents.decode('UTF-8'))
	eatYourBooksParser.print_tag_list(1);
	

	
