def get_keys():
    with open("/Users/ccrowe/github/extract_twitter_favorites/keys.org") as f:
        ck,cv,sk,sv = f.read().split("\n")[:4]
        return (ck,cv,sk,sv)

consumer_key, consumer_secret, access_token, access_token_secret = get_keys()
    
import tweepy

#access_token_secret = get_access_token()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

nike = ""

# Gives anything on timeline, e.g. replies
result = api.user_timeline("Nike",count=1)

# Gives the post info
result = api.get_status("1225203298443153409")


