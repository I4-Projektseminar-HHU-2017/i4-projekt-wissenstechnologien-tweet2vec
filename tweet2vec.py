#!/usr/bin/python3

# Copyright 2017-2018 Matthias Krüger. See the COPYRIGHT
# file at the top-level directory of this distribution.
#
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

import my_config # local file in repo root
import tweepy # http://docs.tweepy.org/en/v3.5.0/getting_started.html
import sys # cheap arg parse
import emoji # pip3  install --user emoji  //  https://github.com/carpedm20/emoji/
from collections import Counter # https://docs.python.org/3/library/collections.html#collections.Counter
import itertools # itertools.combinations


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
        self.cached_mentions = []
        self.cached_hashtags = []

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



def cosine_similarity(vec1, vec2): #int
    # the formular for cosine similarity was taken from slides
    # of the Information Retrieval tutorial by Julia Göretz for the 11th session
    # on 22.01.2016, page 23

    # first item is symbol, prune
    v1 = vec1[1:]
    v2 = vec2[1:]
    assert(len(vec1) == len(vec2) and "ERROR: vec1 and vec2 of different size!")

    numerator = 0
    for iv1, iv2 in zip(v1, v2):
        numerator += (iv1*iv2)

    v1_squared_summed = 0
    for i in v1:
        v1_squared_summed += i**2

    v2_squared_summed = 0
    for i in v2:
        v2_squared_summed += i**2

    prod_sums = v1_squared_summed * v2_squared_summed

    denominator = prod_sums**0.5 # root 

    if (not denominator):
        # this fires if our vectors do not contain common elements
        # print("error: denominator == 0, could probably not find vectors with common symbols")
        return -1
    result = numerator / denominator
    # formula ends here
    return result

def print_similarity(vec1, vec2): #void
    similarity = cosine_similarity(vec1, vec2)
    print("Similarity of '" + vec1[0] + "' and '" + vec2[0] + "' is: " + str(similarity)[0:10])

def print_similarity_from_list(similarity, symbol_1, symbol_2):
    print("Similarity of '" + symbol_1 + "' and '" + symbol_2 + "' is: " + str(similarity)[0:10])


def get_similarities_from_list(list_of_sybols, nested_list):
    # get combinations
    combinations = list(itertools.combinations(list_of_sybols, 2))
    unsorted_sims = []
    for tupel in combinations:
        symbol1 = tupel[0]
        symbol2 = tupel[1]
        vec1 = []
        vec2 = []
        # extract vectors of the two symbols from emojilist
        for i in nested_list:
            # first element of the vector is the symbol
            if i[0] == symbol1:
                vec1 = i
            if i[0] == symbol2:
                vec2 = i
            if vec1 and vec2: # we got everything we need, stop searching
                break
        # once we have the vectors, calc similarity
        sim =  cosine_similarity(vec1, vec2)
        unsorted_sims.append([sim, vec1[0], vec2[0]])
    # sort by similarity
    sorted_sims=sorted(unsorted_sims, reverse=True)

    for i in sorted_sims:
        similarity = i[0]
        symbol_1 = i[1]
        symbol_2 = i[2]

        if similarity > 0: # skip unrelated symbols
            print_similarity_from_list(similarity, symbol_1, symbol_2)


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

        print("Need valid twitter user name.")
        exit(1)

    list_of_tweets=[]

    for i in last_tweets:
        t = Tweet(i) # this creates our own custom wrapper object
#       # debug:
#       print("Tweet:")
#       print(t.message())
#       print(t.emojis())
#       print(t.hashtags())
#       print(t.mentions())
        list_of_tweets.append(t) # fill list with wrapper objs

        #   print(list_of_tweets)

    # generate rough list of emojis contained in tweets
    nested_list_of_emojis = []
    nested_list_of_hashtags = []
    nested_list_of_mentions = []
    for t in list_of_tweets:
        nested_list_of_emojis.append(t.emojis()) # this is a nested list of list of all emojis in one tweet
        nested_list_of_hashtags.append(t.hashtags())
        nested_list_of_mentions.append(t.mentions())

    # flatten nested lists
    list_of_emojis = []
    list_of_hashtags = []
    list_of_mentions = []

    for sublist in nested_list_of_emojis:
        for emoji in sublist:
            list_of_emojis.append(emoji)

    for sublist in nested_list_of_hashtags:
        for hashtag in sublist:
            list_of_hashtags.append(hashtag)

    for sublist in nested_list_of_mentions:
        for mention in sublist:
            list_of_mentions.append(mention)


    # make set
    list_of_emojis = set(list_of_emojis)
    list_of_hashtags = set(list_of_hashtags)
    list_of_mentions = set(list_of_mentions)

    """
        if len(list_of_emojis):
            print("Found emojis:")
            print(list_of_emojis)
        else:
            print("No emojis found :(")

        if len(list_of_hashtags):
            print("Hashtags found:")
            print(list_of_hashtags)
        else:
            print("no #hashtags found.")

        if len(list_of_mentions):
            print("Mentions found:")
            print(list_of_mentions)
        else:
            print("No @mentions found.")
    """



    # build matrix of emojis and tweets containing them
    print("===========")
    emojilist=[]
    for emoji in list_of_emojis: # iterate over emoji
        line = []
        line.append(emoji)
        for tweet in list_of_tweets: # add information on wether the a tweet contains said emoji
            if emoji in tweet.text:
                occurrences = (tweet.text).count(emoji)
                line.append(occurrences)
            else:
                line.append(0)
        emojilist.append(line)


    print("emojis per tweet")

    print("   ", end="") # align properly
    for tweet in list_of_tweets:
        print(tweet.ref.id_str[0:3] + " ", end="")


    print("")
    for sublist in emojilist:
        for data in sublist:
            print(str(data) + "   ", end="")
        print("")


    # build matrix of hashtag and tweets containing them
    print("===========")
    hashtaglist=[]
    for hashtag in list_of_hashtags: # iterate over hashtags
        line = []
        line.append(hashtag)
        for tweet in list_of_tweets: # add information on wether the a tweet contains said emoji
            if hashtag in tweet.text:
                occurrences = (tweet.text).count(hashtag)
                line.append(occurrences)
            else:
                line.append(0)
        hashtaglist.append(line)


    print("hashtags per tweet")

    print("   ", end="") # align properly
    for tweet in list_of_tweets:
        print(tweet.ref.id_str[0:3] + " ", end="")


    print("")
    for sublist in hashtaglist:
        for data in sublist:
            print(str(data) + "   ", end="")
        print("")



    # build matrix of mention and tweets containing them
    print("===========")
    mentionlist=[]
    for mention in list_of_mentions: #iterate over mentions
        line = []
        line.append(mention)
        for tweet in list_of_tweets: # add information on wether the a tweet contains said emoji
            if mention in tweet.text:
                occurrences = (tweet.text).count(mention)
                line.append(occurrences)
            else:
                line.append(0)
        mentionlist.append(line)


    print("mentions per tweet")

    print("   ", end="") # align properly
    for tweet in list_of_tweets:
        print(tweet.ref.id_str[0:3] + " ", end="")

    print("")
    for sublist in mentionlist:
        for data in sublist:
            print(str(data) + "   ", end="")
        print("") # \n


    if len(list_of_emojis):
        get_similarities_from_list(list_of_emojis, emojilist)
    else:
        print("Bailing out: no emojis found")


    if len(list_of_hashtags):
        get_similarities_from_list(list_of_hashtags, hashtaglist)
    else:
        print("Bailing out: no hashtags found")


    if len(list_of_mentions):
        get_similarities_from_list(list_of_mentions, mentionlist)
    else:
        print("Bailing out: no mentions found")


