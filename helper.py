from __future__ import print_function
from twython import Twython, TwythonError
import mmap
import time
#CSV files
#Generic Path
mGeekCodes_Path = '/home/admin/mGeekCodes/'
#For logging all the retweets
tweetedFile = open(mGeekCodes_Path+'tweeted.csv', 'a+')
#For Logging Each Followed Person
all_followed = open(mGeekCodes_Path+'all_followed.csv', 'a+')
#For Keeping a list of current followed
current_followed = open(mGeekCodes_Path+'current_followed.csv', 'a+')

#Mmaps
tweetedMmap = mmap.mmap(tweetedFile.fileno(), 0, access=mmap.ACCESS_READ)
all_followed_Mmap = mmap.mmap(all_followed.fileno(), 0, access=mmap.ACCESS_READ)

banned_accounts = ['todocoders', 'nodenow']

#Twitter Credentials
app_key = "nemYHwbENbRIsqhjECmMGS1wx"
app_secret = "mONLabyAwNIrls1PLn6M7yCroqbA52cuN4Erjs2ZqvH0PMb2I5"
oauth_token = "3678562272-rkoFVgBY1ws0PRwo8RCoznou0Rh8MvfJirViugW"
oauth_token_secret = "lU6LLvoINShdkkPsftM6LL3rZBZL40c2AhIDpD3gd7CvV"

twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)

def handle_tweet(tweet):
    try:
        tweeter = tweet['user']['screen_name']
        text = tweet['text'].encode('utf-8')
        if tweetedMmap.find(text) != -1:
            n=1
        else:
            if all_followed_Mmap.find(tweeter) == -1:
                twitter.create_friendship(screen_name=tweeter)
                print(tweeter+','+str(int(time.time())), file=all_followed)    
                print(tweet)
            if tweeter not in banned_accounts:
                print("New Tweet")
                print(tweet['text'].encode('utf-8'), file=tweetedFile)
                twitter.retweet(id = tweet["id_str"])
                twitter.create_favorite(id = tweet['id_str'])
            else:
                print("Banned Account")
    except TwythonError as e:
        print(e)