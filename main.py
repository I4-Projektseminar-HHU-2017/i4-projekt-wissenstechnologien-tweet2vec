#!/usr/bin/python3

import my_config # local file in repo root
import tweepy # http://docs.tweepy.org/en/v3.5.0/getting_started.html
import sys # cheap arg parse
import emoji # pip3  install --user emoji  //  https://github.com/carpedm20/emoji/
from collections import Counter # https://docs.python.org/3/library/collections.html#collections.Counter



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

class Tweet:
	def __init__(self,tweepyRef): # reference to tweet obj by tweepy
		self.ref = tweepyRef
		self.text = tweepyRef.text
		self.cached_emojis = [] # cache

	def emojis(self): # return list of emojis
		# if we already have the cached results, return these
		if (self.EMOJIS):
			return self.EMOJIS
		emojis=[]
		# emoji.UNICODE_EMOJI taken from https://stackoverflow.com/questions/43146528/how-to-extract-all-the-emojis-from-text
		for char in self.text: # walk text char by char
			if (char in emoji.UNICODE_EMOJI):  # char is recognized as emoji
				emojis.append(char)
		self.EMOJIS = emojis # cache
		return emojis # return list of emojis

	def hashtags(self): # return list of hashtags
		hashtags=[]
		for word in self.text.split(): # split line into words
			if (word[0] == "#") and (len(word) > 1):  # word starts with hashtag and is longer then one char
				hashtags.append(word)
		return hashtags

	def mentions(self): # return list of hashtags
		mentions=[]
		for word in self.text.split(): # split line into words
			if (word[0] == "@") and (len(word) > 1):  # word starts with mention and is longer then one char
				mentions.append(word)
		return mentions

	def message(self):
		return self.text


if __name__ == "__main__":

	API = tweepy_getAPI()
	ARGS = sys.argv

	if (len(ARGS) > 1): # first arg is always script name
		ACC = ARGS[1] # the account we want to get tweets from
		print(ACC)
	else:
		print("WARNING: No arguments passed.")
		exit(1)

	try: 
		# docs of user_timeline() http://tweepy.readthedocs.io/en/v3.5.0/api.html#API.user_timeline
		user_id = API.get_user(ACC).screen_name

		last_tweets = API.user_timeline(user_id, count = 5) # count is the number of tweets to retrieve
	except tweepy.error.TweepError as e:
		# tweepy.error.TweepError: [{'message': 'User not found.', 'code': 50}]
		# can we handles this more gracefully?s
		print("Need valid twitter user name.")
		exit(1)

	for i in last_tweets:
		t = Tweet(i) # this creates our own custom wrapper object
		print("Tweet:")
		print(t.message())
		print(t.emojis())
		print(t.hashtags())
		print(t.mentions())

		print("")

		print("\n\n\n")

