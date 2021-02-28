#import dependencies
import httpx
from bs4 import BeautifulSoup

#find target
response = httpx.get('https://incubator.wikimedia.org/wiki/Wp/enm/Frogge')

#get content from target
soup = BeautifulSoup(response.content, 'html.parser')

#find thing
header = soup.find('title').get_text()
body_text = soup.find(id = 'mw-content-text')

#print content
print(header + '\n')
for text in body_text:
    print(text.get_text())
    print('\n')