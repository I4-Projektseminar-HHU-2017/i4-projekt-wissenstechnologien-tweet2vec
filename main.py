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
		# caches, avoid recomputation
		self.cached_emojis = []
		self.cached_hashtags = []
		self.cached_mentions = []

	def emojis(self): # return list of emojis
		# if we already have the cached results, return these
		if (self.cached_emojis):
			return self.cached_emojis
		emojis=[]
		# emoji.UNICODE_EMOJI taken from https://stackoverflow.com/questions/43146528/how-to-extract-all-the-emojis-from-text
		for char in self.text: # walk text char by char
			if (char in emoji.UNICODE_EMOJI):  # char is recognized as emoji
				emojis.append(char)
		self.cached_emojis = emojis # cache
		return emojis # return list of emojis

	def hashtags(self): # return list of hashtags
		if (self.cached_hashtags):
			return self.cached_hashtags
		hashtags=[]
		for word in self.text.split(): # split line into words
			if (word[0] == "#") and (len(word) > 1):  # word starts with hashtag and is longer then one char
				hashtags.append(word)
		self.cached_hashtags = hashtags
		return hashtags

	def mentions(self): # return list of mentions
		if (self.cached_mentions):
			return self.cached_mentions
		mentions=[]
		for word in self.text.split(): # split line into words
			if (word[0] == "@") and (len(word) > 1):  # word starts with mention and is longer then one char
				mentions.append(word)
		self.cached_mentions = mentions
		return mentions

	def message(self):
		return self.text


if __name__ == "__main__":

	API = tweepy_getAPI()
	ARGS = sys.argv

	if (len(ARGS) > 1): # first arg is always script name
		ACC = ARGS[1] # the account we want to get tweets from
		NUM_TWEETS = 10  if (len(ARGS) == 2) else ARGS[2] # default to retrieving 20 tweets if no number passed as 2nd param
	else:
		print("WARNING: No arguments passed.")
		exit(1)

	try: 
		# docs of user_timeline() http://tweepy.readthedocs.io/en/v3.5.0/api.html#API.user_timeline
		user_id = API.get_user(ACC).screen_name

		last_tweets = API.user_timeline(user_id, count = NUM_TWEETS) # count is the number of tweets to retrieve
	except tweepy.error.TweepError as e:
		# tweepy.error.TweepError: [{'message': 'User not found.', 'code': 50}]
		# can we handles this more gracefully?s
		print("Need valid twitter user name.")
		exit(1)

	list_of_tweets=[]

	for i in last_tweets:
		t = Tweet(i) # this creates our own custom wrapper object
#		print("Tweet:")
#		print(t.message())
#		print(t.emojis())
#		print(t.hashtags())
#		print(t.mentions())
		list_of_tweets.append(t) # tweet obj

	print(list_of_tweets)

	# generate rough list of emojis contained in tweets
	bad_list_of_emojis =[]
	for t in list_of_tweets:
		bad_list_of_emojis.append(t.emojis())

	# feed emoji sublists into one unified list
	print(bad_list_of_emojis) # [[], ['💰', '🐝', '‼', '👀'], ['💰', '💰', '\U0001f91e', '🏼'], ['🤔'], ['💝']]
	list_of_emojis = []
	for sublist in bad_list_of_emojis:
		for emoji in sublist:
#		print(x)
			list_of_emojis.append(emoji)

	# make set
	list_of_emojis = set(list_of_emojis)
	print(list_of_emojis)


	# build matrix of emojis and tweets containing them
	print("===========")
	glob=[]
	for emoji in list_of_emojis: #iterate over emoji
		line = []
		line.append(emoji)
		for tweet in list_of_tweets: # add information on wether the a tweet contains said emoji
			if emoji in tweet.text:
				line.append(1)
			else:
				line.append(0)
		glob.append(line)

	for x in glob:
		print(x)
