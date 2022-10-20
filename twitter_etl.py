from distutils.command.config import config
import tweepy
import pandas as pd
import json
from datetime import datetime
import s3fs


def run_twitter_etl():
    access_key = config.ACCESS_KEY
    access_secret = config.ACCESS_SECRET
    consumer_key = config.CONSUMER_KEY
    consumer_secret = config.CONSUMER_SECRET


    # Twitter Authentication
    auth = tweepy.OAuthHandler(access_key , access_secret)
    auth.set_access_token(consumer_key , consumer_secret)

    #Creating an API object
    api = tweepy.API(auth)

    tweets = api.user_timeline(screen_name='@elonmusk',count=200 , include_rts= False,tweet_mode='extended')

    tweet_list = []
    for tweet in tweets:
        text = tweet._json["full_text"]

        refind_tweet = {"user" : tweet.user.screen_name, 
        "text" : text , 
        "favorite_count" : tweet.favorite_count, 
        'retweet_count' : tweet.retweet_count,
        'created_at' : tweet.created_at}

        tweet_list.append(refind_tweet)

    df = pd.DataFrame(tweet_list)
    df.to_csv(Config.S3BUCKET +"elonmust_twitter_data.csv")