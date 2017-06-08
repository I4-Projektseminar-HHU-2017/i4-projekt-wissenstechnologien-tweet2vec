#!/usr/bin/python3

import my_config # local file in repo root
import tweepy # http://docs.tweepy.org/en/v3.5.0/getting_started.html
import sys # cheap arg parse

def tweepy_getAPI(): # log in via auth token and return api
	KEY = my_config.consumer_key
	SECRET = my_config.consumer_secret
	TOKEN = my_config.access_token
	TOKEN_SECRET = my_config.access_token_secret
	# Login code was taken from http://docs.tweepy.org/en/v3.5.0/getting_started.html#hello-tweepy
	auth = tweepy.OAuthHandler(KEY, SECRET)
	auth.set_access_token(TOKEN, TOKEN_SECRET)
	api = tweepy.API(auth)
	return api


API = tweepy_getAPI()

ARGS = sys.argv

if (len(ARGS) > 1): # first arg is always script name
	ACC = ARGS[1] # the account we want to get tweets from
	print(ACC)
else:
	print("WARNING: No arguments passed.")
	print("Need Twitter Account name.")
	exit()


# @TODO: check that the passed arg is a valid twitter account name!
# @TODO: check if we need to catch exception thrown if (number of tweets to retrieve) > (number of tweets by user)

# docs of user_timeline() http://tweepy.readthedocs.io/en/v3.5.0/api.html#API.user_timeline
user_id = API.get_user(ACC).screen_name

last_tweets = API.user_timeline(user_id, count = 5) # count is the number of tweets to retrieve

for i in last_tweets:
	print(i)
	print("\n\n\n")

