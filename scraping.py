import pandas as pd
import tweepy

consumer_key = 'XXXXXXXXXXXXXXXXXXXXXXX'
consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXX'
client_secret = "XXXXXXXXXXXXXXXXXXXXXXX"
access_token = 'XXXXXXXXXXXXXXXXXXXXXXX'
access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXX'

# Authenticate to Twitter

# Twitter authentication and the connection to Twitter API
client = tweepy.Client(consumer_key=consumer_key,
                    consumer_secret=consumer_secret, 
                    access_token=access_token, 
                    access_token_secret=access_token_secret)


#fields you wish to scrape
tweet_fields = ['id', 'text', 'created_at', 'public_metrics', 'author_id', 'attachments', 'entities']
scraping = client.search_recent_tweets(query='#startup',  tweet_fields=tweet_fields, user_fields = 'username', user_auth=True, expansions = ['author_id'])
#turning it into data format
tweets = scraping.data
#intial structure that will later be turned into a dataframe
tweet_data = []
#extracting user data from scraping, to get any more items besides default id, name, username, add them into the userfields section above.
users = {u['id']: u for u in scraping.includes['users']}
for tweet in tweets:
    if users[tweet.author_id]:
        user = users[tweet.author_id]
    try: 
        media = tweet.entities['urls'][0]['expanded_url']
    except:
        media = None

    tweet_data.append({
        'Name': user['name'],
        'Handle': user['username'],
        'Media URL': media,
        'Tweet ID': tweet.id,
        'Retweets': tweet.public_metrics['retweet_count'],
        'Likes': tweet.public_metrics['like_count'],
        'Comments': tweet.public_metrics['reply_count'],
        'Views': tweet.public_metrics['impression_count'],
        'Tweet URL': f"https://twitter.com/i/status/{tweet.id}",
        'Profile Link': f"https://twitter.com/{user['username']}",
        'Post Body': tweet.text,
        'Date': tweet.created_at.date(),
        'Timestamp': tweet.created_at
    })

df = pd.DataFrame(tweet_data)
print(df)
df.to_csv('tweets.csv', index=False, encoding='utf-16', sep='\t')
print("ran")
