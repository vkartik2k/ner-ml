from twitterscraper import query_tweets
import datetime as dt
import pandas as pd

textfile = open('delhi_local_areas.csv')
data = []
for line in textfile:
    row_data = line.strip("\n")
    data.append(row_data)

tweets = []

def extractTweets(location):
    tweets = query_tweets(location + ", Delhi, covid", limit=1, lang='english')
    df=pd.DataFrame(t.__dict__ for t in tweets)
    try :
        df1 = df.text
        df1.to_csv('output_tweeter.csv', mode='a', header=False)
    except :
        print('error')

for i in range(len(data)) :
    extractTweets(data[i])
        
print(tweets)