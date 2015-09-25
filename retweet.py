#Import TwythonError now too!
from __future__ import print_function
from twython import Twython, TwythonError
import mmap

app_key = "nemYHwbENbRIsqhjECmMGS1wx"
app_secret = "mONLabyAwNIrls1PLn6M7yCroqbA52cuN4Erjs2ZqvH0PMb2I5"
oauth_token = "3678562272-rkoFVgBY1ws0PRwo8RCoznou0Rh8MvfJirViugW"
oauth_token_secret = "lU6LLvoINShdkkPsftM6LL3rZBZL40c2AhIDpD3gd7CvV"

tweetedFile = open('/home/admin/mGeekCodes/tweeted.csv', 'a+')
mapread = mmap.mmap(tweetedFile.fileno(), 0, access=mmap.ACCESS_READ)

banned_accounts = ['todocoders', 'nodenow']
naughty_words = [" -RT", "HackerEarth", "Looking for", "Jobs", "job", "prizes", "todocoders"]
good_words = ["%23CodeBetter", "%23SoftwareCode", "%23AndroidCode", "%23PythonCode", "%23JavaCode", "%23Coder", "%23Coding", "%23ArduinoCode", "%23BetterAndroid", "%23CodeALot"]
filter = " OR ".join(good_words)
blacklist = " -".join(naughty_words)
keywords = filter + blacklist

twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)

#Setting Twitter's search results as a variable
search_results = twitter.search(q=keywords, count=100, result_type='mixed')
try:
    for tweet in search_results["statuses"]:
         text = tweet['text'].encode('utf-8')
         if mapread.find(text) != -1:
             n=1
         else:
             print(tweet)
             if tweet['user']['screen_name'] not in banned_accounts:
                 print("New Tweet")
                 print(tweet['text'].encode('utf-8'), file=tweetedFile)
                 twitter.retweet(id = tweet["id_str"])
             else:
                 print("Banned Account")
except TwythonError as e:
    print(e)
print(len(search_results['statuses']))