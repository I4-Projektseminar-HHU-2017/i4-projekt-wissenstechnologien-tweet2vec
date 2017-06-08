#!/usr/bin/python3

import my_config # local file in repo root
import tweepy # http://docs.tweepy.org/en/v3.5.0/getting_started.html


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
