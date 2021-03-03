#dependencies
import tweepy
import cfg

#authentication
#set access token to enable use of twitter api
auth = tweepy.OAuthHandler(cfg.oauth_consumer_key, cfg.oauth_consumer_secret)
auth.set_access_token(cfg.access_token, cfg.access_token_secret)

#set instance of Twitter API wrapper
api = tweepy.API(auth)

#recieves quote text, posts a tweet with that quote text
def post(message):
    api.update_status(message)