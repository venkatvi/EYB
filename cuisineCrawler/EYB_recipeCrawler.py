import re
import requests
import hashlib
from urllib2 import URLError, HTTPError
from HTMLParser import HTMLParser
from pymongo import Connection
from optparse import OptionParser
#from xml.etree import cElementTree as etree

class Downloader:
        '''
        Class to retrieve HTML code from a specific page
        '''

        def __init__(self,url):
                self.url = url
                self.contents = ''
#                self.tb = etree.TreeBuilder()

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
        tag_type = ""
        list_index = 0
        is_page_root = 0
        
        
        def __init__(self):
                name = ''
                text = ''
                first_child = 0
                parent = 0
                next_sibling = 0
                closed = 0
                depth = 0
                attrs = []
                tag_type = ""
                list_index = 0
                is_page_root = 0


        def __eq__(self, other):
                for attr in ['name', 'text', 'first_child', 'parent', 'next_sibling', 'closed', 'depth', 'attrs', 'tag_type']: 
                        v1, v2 = [getattr(obj, attr, _NOTFOUND) for obj in [self,other]]
                        if v1 is _NOTFOUND or v2 is __NOTFOUND:
                                return False
                        elif v1 != v2:
                                return False
                return True

        def update_tag_info(self):
                for name, value in self.attrs:
                        if name == 'class':
                                if value == 'listing recipe hrecipe ' :
                                        self.tag_type = "recipes"
                                        break
                                elif value == "listing" :
                                        self.tag_type = "cookbooks"
                                        break
                        if self.name == 'ul' and name == 'class' and value == 'pages':
                                self.is_page_root = 1
                                break

        def get_tag_info_str(self):
                c ,p ,s = 'none', 'none', 'none'
                if self.first_child != 0:
                        c = self.first_child.name
                if self.parent != 0:
                        p = self.parent.name
                if self.next_sibling != 0:
                        s = self.next_sibling.name

                for name, value in self.attrs:
                        if name == 'class':
                                if value == 'listing recipe hrecipe ' :
                                        self.tag_type = "recipes"
                                        break
                                elif value == 'listing': 
                                        self.tag_type = "cookbooks"
                                        break
                        if self.name == 'ul' and name == 'class' and value == 'pages':
                                self.is_page_root = 1
                                break

                formatString = u" Name = {}, Text = {} \n Parent = {}, First Child = {}, Next Sibling = {} \n Closed = {}, Depth = {} \n Type = {} \n\n\n".format(self.name, self.text, p, c, s, self.closed, self.depth, self.tag_type)
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
        def initalize(self):
                self.tag_list = []
                self.depth = 0
                self.previous_tag = 'none'
                self.mode = 'nonsilent'

        def cleanup(self):
                del self.tag_list[:]

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
                t.update_tag_info()
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
                t.update_tag_info()
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

        def get_tag_list(self):
                return self.tag_list;


class EatYourBooksItem:
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
        item_str = ""
        item_url = ""
        rating = 0
        notes_str = ""
        notes_url = ""
        online_url = ""
        check_sum = ""
        item_type = ""
        '''
        Used inner classes to test anonymous classes, their callability and access in python. 
        Ignore this design. 
        '''
        class BookData:
                shelf_status = ""
                source_str = ""
                source_url = ""
                author_str = ""
                author_url = ""
                isbn = ""
                cover_type = ""
                published_country = ""
                published_date = ""
                def __call__(self):
                        shelf_status = "";

        def __init__(self, tag_list, start_index, end_index, item_type):
                self.item_type = item_type
                self.book_data = self.BookData()
                child_nodes=filter(lambda x: x.depth == tag_list[start_index].depth + 1, tag_list[start_index: end_index ])
                if len(child_nodes) == 3:
                        self.parse_book_data(tag_list, child_nodes[1].list_index, end_index-1)

        def parse_book_data(self, tag_list, start_index, end_index):
                child_nodes = filter(lambda x: x.depth == tag_list[start_index].depth + 1, tag_list[start_index: end_index])
                # Recipes: bookshelf_status, book_title, feedback, meta.
                # Cookbooks: bookshelf_status, feedback, meta.
                child_tags_count = 4 if self.item_type == "recipes" else  3
                if len(child_nodes) == child_tags_count:
                        index = 0
                        if self.item_type == "recipes": 
                                self.parse_bookshelf_status(tag_list, child_nodes[0].list_index, child_nodes[1].list_index)
                                index = 1        
                        self.parse_book_title(tag_list, child_nodes[index].list_index, child_nodes[index + 1].list_index)
                        self.parse_feedback(tag_list, child_nodes[index + 1].list_index, child_nodes[index + 2].list_index)
                        self.parse_meta(tag_list, child_nodes[index + 2].list_index, end_index)

        def parse_bookshelf_status(self, tag_list, start_index, end_index):
                child_nodes = filter(lambda x: x.depth == tag_list[start_index].depth + 1, tag_list[start_index: end_index - 1])
                #how to handle? 
                #this tag is empty for recipes. 
                '''
                <div class="bookshelf-status">
                        <button class="btn btnshelf" entityid="11997" entitytype="1" ismag="False" title="Add to your Bookshelf">Bookshelf</button>
                    </div>
                '''
                #this is getting parsed in rating

        def parse_book_title(self, tag_list, start_index, end_index):
                child_nodes = filter(lambda x: x.depth == tag_list[start_index].depth + 1, tag_list[start_index:end_index -1])
                child_tags_count = 2 if self.item_type == "recipes" else 3
                if len(child_nodes) == child_tags_count:
                        index = 0
                        if self.item_type == "cookbooks":
                                self.parse_bookshelf_status(tag_list, child_nodes[0].list_index, child_nodes[1].list_index)
                                index = 1
                        self.parse_title_fn(tag_list, child_nodes[index ].list_index, child_nodes[index + 1].list_index)
                        self.parse_from_by(tag_list, child_nodes[index + 1].list_index, end_index)
                                  
        def parse_feedback(self, tag_list, start_index, end_index):
                child_nodes = filter(lambda x: x.depth == tag_list[start_index].depth + 1, tag_list[start_index:end_index - 1])
                if len(child_nodes) == 3:
                        self.parse_rating(tag_list, child_nodes[0].list_index, child_nodes[1].list_index)
                        self.parse_notes(tag_list, child_nodes[1].list_index, child_nodes[2].list_index)
                        self.parse_online(tag_list, child_nodes[2].list_index, end_index)

        def parse_meta(self, tag_list, start_index, end_index):
                child_nodes = filter(lambda x: x.depth == tag_list[start_index].depth + 1, tag_list[start_index:end_index])
                if len(child_nodes) > 0: 
                        self.parse_categories(tag_list, child_nodes[0].list_index, child_nodes[1].list_index)
                if self.item_type == "recipes" and len(child_nodes) > 1:
                        self.parse_ingredients(tag_list, child_nodes[1].list_index, child_nodes[2].list_index)
                if self.item_type == "cookbooks" and len(child_nodes) > 1:
                        self.parse_isbn(tag_list, child_nodes[1].list_index, child_nodes[2].list_index)
                index = 2
                if len(child_nodes) == 4: #sometimes an empty li tag is inserted. 
                        index = 3;
                self.parse_index_status(tag_list, child_nodes[index].list_index, end_index)
                if self.item_type == "recipes" and (len(self.categories) == 0 or len(self.ingredients) == 0):
                        print "ERROR"
                elif self.item_type == "cookbooks" and (len(self.categories) == 0 or self.book_data.isbn == ""):
                        print "POT ERROR"
                else:
                        print self.ingredients
                        print self.categories
                        print self.book_data.isbn
                        print self.is_indexed
        def parse_title_fn(self, tag_list, start_index, end_index):
                item_url = ""
                item_str = ""
                child_node = tag_list[start_index + 1]
                if child_node.name == 'a':
                        for name, value in child_node.attrs:
                                if name == 'href': 
                                        item_url = value
                        item_str = child_node.text
                self.item_url = item_url
                self.item_str = item_str
                

        def parse_from_by(self, tag_list, start_index, end_index):
                child_nodes = filter(lambda x: x.name == 'i', tag_list[start_index:end_index - 1])
                source_str = ""
                author_str = ""
                author_url = ""
                for child_node in child_nodes:
                        fromby_text = child_node.text
                        fromby_text = fromby_text.strip()
                        fromby_text = fromby_text.strip('&nbsp;')
                        
                        grand_child_node = tag_list[child_node.list_index + 1]
                        for name, value  in grand_child_node.attrs:
                                if grand_child_node.name == 'span' and name == 'class' and value == 'title':
                                               source_str = grand_child_node.text
                                if grand_child_node.name == 'a' and name == 'class' and value == 'author':
                                        author_str = grand_child_node.text
                                if grand_child_node.name == 'a' and name == 'href':
                                        author_url = value
                if self.book_data is None:
                        self.book_data = self.BookData()
                self.book_data.source_str = source_str
                self.book_data.author_str = author_str
                self.book_data.author_url = author_url
                               
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
        def parse_isbn(self, tag_list, start_index, end_index):
                child_node = tag_list[start_index + 1]
                if child_node.text == 'ISBN:':
                        isbn_text = tag_list[start_index].text
                        isbn_text = isbn_text.strip()
                        isbn_contents = isbn_text.split('\r\n');
                        if len(isbn_contents) > 0: 
                                temp1 = isbn_contents[0].split(' ');
                                isbn = temp1[0].strip()
                                self.book_data.isbn = isbn
                                if len(temp1) > 1:
                                        cover_type = temp1[1].strip()
                                        self.book_data.cover_type = cover_type
                                if len(isbn_contents) > 1:
                                        published_country = isbn_contents[1].strip()
                                        self.book_data.published_country = published_country
                                if len(isbn_contents) > 2:
                                        published_year = isbn_contents[2].strip()
                                        self.book_data.published_date = published_year
                
        def parse_index_status(self, tag_list, start_index, end_index):
                child_node = tag_list[start_index + 1]
                if child_node.name == 'b' and child_node.text == 'Member Indexed': 
                        self.is_indexed = 1
                
        def parse_rating(self, tag_list, start_index, end_index):
                child_node = tag_list[start_index + 1]
                if child_node.name == 'span':
                        for name, value in child_node.attrs:
                                if name == 'rating':
                                        self.rating = float(value)
                                if name == 'entitytype':
                                        self.type = value
                                if name == 'entityid':
                                        self.id = int(value)
        def parse_notes(self, tag_list, start_index, end_index):
                child_node = tag_list[start_index + 1]
                if child_node.name == 'a':
                        for name, value in child_node.attrs:
                                if name == 'href':
                                        self.notes_url = value
        def parse_online(self, tag_list, start_index, end_index):
                child_node = tag_list[start_index + 1]
                if child_node.name == 'a':
                        for name, value in child_node.attrs:
                                if name == 'href':
                                        self.online_url = value
        def print_item(self):
                categories_str = ', '.join(self.categories)
                ingredients_str = ', '.join(self.ingredients)

                formatString = u" Id = {} \n Type = {} \n Is Indexed = {} \n Categories = {} \n Ingredients = {} \n Shelf Status = {} \n Name = {} \n Url = {} \n Source = {} \n Source Url = {} \n Author = {} \n Author Url = {} \n Rating = {} \n Notes Url = {} \n Online Url = {} \n\n\n".format(self.id, self.type, self.is_indexed, categories_str, ingredients_str, self.book_data.shelf_status, self.item_str, self.item_url, self.book_data.source_str, self.book_data.source_url, self.book_data.author_str, self.book_data.author_url, self.rating, self.notes_url, self.online_url)
                return formatString.encode('UTF-8')            

class EatYourBooksFilter:
        root_url = ""
        urls = []
        items = {}
        cuisine = ""
        item_type = ""

        def __init__(self, url, cuisine, item_type):
                self.root_url = url
                self.urls = []
                self.urls.append(url)
                self.items = {}
                self.cuisine = cuisine 
                self.item_type = item_type

        def parse_items(self, url):
                parser = EatYourBooksParser()
                parser.initalize()

                downloader = Downloader(url)
                downloader.download()

                parser.feed(downloader.contents.decode('UTF-8'))
                current_tag_list = parser.get_tag_list()

                if (url == self.root_url):
                        self.parse_pagination(current_tag_list)
                for url in self.urls:
                        if url == self.root_url:
                                self.parse_page_by_url("", current_tag_list)
                        else:
                                self.parse_page_by_url(url, None)
                        #print "Recipes So Far: " + str(len(self.recipes))
                
        def parse_pagination(self, tag_list):
                pagination_root_node = filter(lambda x: x.name == 'ul' and x.is_page_root, tag_list)
                if(len(pagination_root_node) == 1):
                        self.parse_page_urls(pagination_root_node[0].list_index, tag_list)
                
        def parse_page_urls(self, page_root_index, tag_list):
                root_url = 'http://www.eatyourbooks.com'
                last_page_index = 0
                page_root_depth = tag_list[page_root_index].depth
                for i in range(page_root_index+2, len(tag_list)-1):
                        if ((i-page_root_index+2) % 2 == 1):
                                #ignore li
                                continue
                        tag = tag_list[i]
                        if (tag.depth == page_root_depth + 2):
                                for name, value in tag.attrs:
                                        if tag.name == 'a' and name == 'href':
                                                m = re.search('\d+', tag.text)
                                                if m is not None:
                                                        pg = m.group(0)
                                                        last_page_index = int(pg)
                                                        new_page_url = ''.join([ root_url, value])
                                                        if new_page_url not in self.urls:
                                                                self.urls.append(new_page_url)
                for i in range(2, last_page_index):
                        page_url = ''.join([root_url, '/', self.item_type, '/', self.cuisine, '/', str(i)])
                        if page_url not in self.urls:
                                self.urls.append(page_url)
                                
        def parse_page_by_url(self, url="", tag_list=None):
                ptag_list = [];
                parser = None
        #        print "URL to parse: " + url
                if url == "" and tag_list == None:
                        return
                if url != "":
                        parser = EatYourBooksParser()
                        parser.initalize()

                        downloader = Downloader(url)
                        downloader.download()

                        parser.feed(downloader.contents.decode('UTF-8'))
                        ptag_list = parser.get_tag_list()
                else:
                        ptag_list = tag_list
                
                item_root_nodes = filter(lambda x: x.name == 'li' and x.tag_type == self.item_type, ptag_list)
                if len(item_root_nodes) > 0:
                        for i in range(0, len(item_root_nodes)-1):
                                ps = item_root_nodes[i].list_index
                                pe = item_root_nodes[i+1].list_index
                                item = EatYourBooksItem(ptag_list, item_root_nodes[i].list_index, item_root_nodes[i+1].list_index, self.item_type)
                                self.add_item(item)
                                

                        ps = item_root_nodes[len(item_root_nodes)-1].list_index
                        
                        item_end_nodes = filter(lambda x: x.depth == item_root_nodes[-1].depth, ptag_list[ps+1:])
                        end_index = len(ptag_list)-1;
                        if len(item_end_nodes) <= 0:
                                print "ERRRRRRRORRR"
                        else:
                                end_index = item_end_nodes[0].list_index
                        item = EatYourBooksItem(ptag_list, item_root_nodes[len(item_root_nodes)-1].list_index, end_index, self.item_type)
                        self.add_item(item)
                else:
                        print "No items found for " + url                
                del ptag_list[:]

        def add_item(self,item):
                item_contents = item.print_item()
                item_checksum = hashlib.md5(item_contents).hexdigest()

                if item_checksum in self.items.keys():
                        f = open('repeated_items.txt', 'a')
                        pstr = "Items already exists:" + str(item.id) + " " + item.print_item() + "\n"
                        f.write(pstr.encode('UTF-8'))
                        f.close()
                else:
                        item.check_sum = item_checksum
                        self.items[item_checksum]=item


class EatYourBooksDB:
        connection = None
        db = None
        item_collection = None
        def __init__(self, dbname, ipaddress, item_type):
                self.connection = Connection(ipaddress, 27017)
                db_name = dbname;
                collection_name = item_type; 
                self.db = self.connection[db_name]
                self.item_collection = self.db[collection_name]
        
        def add_item(self, item, cuisine, item_type):
                new_item =  {"id": item.id,
                                "type": item.type,
                                "indexed": item.is_indexed,
                                "item_str": item.item_str,
                                "item_url": item.item_url,
                                "rating": item.rating,
                                "notes_str": item.notes_str,
                                "notes_url": item.notes_url,
                                "online_url": item.online_url,
                                "author_str": item.book_data.author_str,
                                "author_url": item.book_data.author_url,
                                "source_url": item.book_data.source_url,
                                "source_str": item.book_data.source_str,
                                "cuisine": cuisine,
                                "ingredients": item.ingredients,
                                "categories": item.categories,
                                "isbn": item.book_data.isbn,
                                "published_year": item.book_data.published_date,
                                "published_country": item.book_data.published_country,
                                "cover_type" : item.book_data.cover_type,
                                "check_sum" : item.check_sum
                               }                
                self.item_collection.save(new_item)
if __name__ == '__main__':
        ipaddress = ""
        itemtype = ""
        urllinks = ""
        parser = OptionParser()
        parser.add_option("-i", "--ipaddress", dest="ipaddress", help="ipaddress of remote mongodbserver", default="localhost")
        parser.add_option("-t", "--itemtype", dest="itemtype", help="item type i.e. recipes/cookbooks to be parsed and added", default="recipes")
        parser.add_option("-u", "--urllinks", dest="urllinks", help="text file containing urls to be parsed", default="recipe_links.txt")
        parser.add_option("-d", "--database", dest="db", help="database name to store parsed data. Database should contain collections of the name given in --itemtype option", default="EatYourBooksDB")

        options, arguments = parser.parse_args()
        print "Command Line Inputs: " 
        print "ipaddress: " + options.ipaddress
        print "item type: " + options.itemtype
        print "links file: " + options.urllinks        
        print "db name: " + options.db
        
        
        urls = [line.strip() for line in open(options.urllinks)]
        for url in urls:
                start_url = url #"http://www.eatyourbooks.com/recipes/indian"
                m = re.search('\/[a-z-]+$', start_url);
                cuisine = m.group(0)
                cuisine = cuisine.strip('/');
                print "Cuisine: " + cuisine 
                eatyourbooksParser = EatYourBooksFilter(start_url, cuisine, options.itemtype)
                eatyourbooksParser.parse_items(start_url)
                print 'Cuisine:' + cuisine + ' Item Collection: ' + str(len(eatyourbooksParser.items))
        
                
                db = EatYourBooksDB(options.db, options.ipaddress, options.itemtype)
                for key, item in eatyourbooksParser.items.iteritems():
                        db.add_item(item, cuisine, options.itemtype)

