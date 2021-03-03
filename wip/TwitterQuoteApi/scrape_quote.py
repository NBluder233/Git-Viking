#dependencies
import random
import httpx
from bs4 import BeautifulSoup

#Get website content
content = httpx.get('http://quotes.toscrape.com/').content

#convert to soup
soup = BeautifulSoup(content, 'html.parser')

#get collection of quotes
quotes = soup.find_all(class_ = 'quote')

#get random quote and pull relevant data (quote, author)
random_index = random.randint(0, 3)

quote_text = quotes[random_index].find(class_ = 'text').get_text(strip = True)
quote_author = quotes[random_index].find(class_ = 'author').get_text(strip = True)

#return string with quote and author
def scrape():
    return (quote_text + " - " + quote_author)