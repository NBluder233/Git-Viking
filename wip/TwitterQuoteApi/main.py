from fastapi import FastAPI
import scrape_quote
import post_tweet

app = FastAPI()

@app.get('/postquote')
def postquote():
    quote = scrape_quote.scrape()
    post_tweet.post(quote)
    return {'message' : 'success'}
