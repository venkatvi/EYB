import requests;

r = requests.get('http://www.eatyourbooks.com/recipes/indian')
contents = r.text
contents = contents.encode('utf-8')
f = open('myfile.txt','w')
f.write(contents)

