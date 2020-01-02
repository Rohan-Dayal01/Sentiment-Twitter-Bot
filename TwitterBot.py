import sys
import simple_twit
import tweepy
from tweepy import OAuthHandler
import sys, os, json, webbrowser
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def main():
    # This call to simple_twit.create_api will create the api object that
    # Tweepy needs in order to make authenticated requests to Twitter's API.
    # Do not remove or change this function call.
    # Pass the variable "api" holding this Tweepy API object as the first
    # argument to simple_twit functions.
    api = simple_twit.create_api()
    # YOUR CODE BEGINS HERE
    simple_twit.version()
    CONFIG_FILE = "twitter_bot.config"
    consumer_key = "#################";
    consumer_secret = "################"
    f = open(CONFIG_FILE, "r")
    config = json.load(f)
    access_token = config["access_token"]
    access_token_secret = config["access_secret"]
    f.close()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    myListener = MyStreamListener()
    myStream = tweepy.Stream(auth, listener = myListener)
    keywords  = ['Yankees', 'Cole', 'Cashman']
    myStream.filter(track = keywords)
    tweets = myListener.tweets#tweets is a list of string objects now
    #print(tweets)
    #tweets.extend(simple_twit.get_home_timeline(api, 3))
    sid = SentimentIntensityAnalyzer()
    aggs=[0,0,0,0]#element 0 is total compound, element 1 is total negative, element 2 is total neutral, element 3 is total positive
    for tweet in tweets:
        #print(tweet)
        ss = sid.polarity_scores(tweet)
        x=0
        for k in sorted(ss):#k is key
            #print('{0}: {1}, '.format(k, ss[k]), end='')
            #print(ss[k])
            #print()
            aggs[x]+=ss[k]
            x+=1
    #print("AGGREGATE")
    #print(aggs[0])
    #print(aggs[1])
    #print(aggs[2])
    #print(aggs[3])
    aggtext = ("For the query using keywords " + str(keywords) + ", the average sentiment values are as follows. Compound "+str(aggs[0]/15.0)+", negative " + str(aggs[1]/15.0)+", neutral " + str(aggs[2]/15.0)+", positive " + str(aggs[3]/15.0))
    print(aggtext)
    #for tweet in tweets:
        #print("MY PRINT " + tweet)
        #simple_twit.send_tweet(api,tweet)
    simple_twit.send_tweet(api, aggtext)

class MyStreamListener(tweepy.StreamListener):
    tweets = []
    starttym = time.time()
    def on_data(self, data):#data comes as a dictionary with each attribute being a separate key
        """if(len(tweets)<=100):
            try:
                print(data.full_text)
                tweets.append(data.full_text)
            except (BaseException, e):
                print("Failed ondata, ", e)"""
        #print(type(data))
        onetweetdict = json.loads(data)
        #print(onetweetdict)
        #print()
        #if("RT @" in data.split(',"text":"')[1].split('","source')[0]):
            #pass
        if('text' in onetweetdict):
            if("RT @" in onetweetdict['text']):
                pass
            elif((len(self.tweets)<10)):#ensures that tweet collection does not last for over 30 seconds
                #print(data.split(',"text":"')[1].split(',"source"')[0])# CURRENTLY RUNNING INTO AN ERROR THAT THE SPLITTING IS NOT WORKING CORRECTLY. INVESTIGATE
                #self.tweets.append(data.split(',"text":"')[1].split(',"source')[0])#Tweet data is output as a string, but with dictionary format
                self.tweets.append(onetweetdict['text'])
                print(onetweetdict['text'])
            else:
                return False

                
if __name__ == "__main__":
       main()
