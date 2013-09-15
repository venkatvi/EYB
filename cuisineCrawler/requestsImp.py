import requests

r = requests.get('http://www.eatyourbooks.com/recipes/indian')

print ('Status: ', r.status_code)
print ('Headers: ', r.headers['content-type'])
contents = r.text
contents = contents.encode('UTF-8')
f = open ('contents_requestsImp.txt', 'w');
f.write (contents)
print ('Encoding: ', r.encoding)
print ('JSON: ', r.json)
