#!/usr/bin/python3

import my_config # local file in repo root
import tweepy # http://docs.tweepy.org/en/v3.5.0/getting_started.html
import sys # cheap arg parse
import emoji # pip3  install --user emoji  //  https://github.com/carpedm20/emoji/

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

def extract_emojis(string): # return list of emojis
	emojis=[]
# emoji.UNICODE_EMOJI taken from https://stackoverflow.com/questions/43146528/how-to-extract-all-the-emojis-from-text
	for char in string: # walk text char by char
		if (char in emoji.UNICODE_EMOJI):  # char is recognized as emoji
			emojis.append(char)
	return emojis # return list of emojis


def extract_hashtags(string): # return list of hashtags
	hashtags=[]
	for word in string.split(): # split line into words
		if (word[0] == "#") and (len(word) > 1):  # word starts with hashtag and is longer then one char  
			hashtags.append(word)
	return hashtags


def extract_mentions(string): # return list of hashtags
	mentions=[]
	for word in string.split(): # split line into words
		if (word[0] == "@") and (len(word) > 1):  # word starts with mention and is longer then one char  
			mentions.append(word)
	return mentions


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
	TEXT = i.text
	print("Tweet:")
	print(TEXT) # tweet.text
	print("")
	print("Emojis: " + str(extract_emojis(TEXT)))
	print("Hashtags: " + str(extract_hashtags(TEXT)))
	print("Mentions: " + str(extract_mentions(TEXT)))


	print("\n\n\n")

