def get_keys():
    with open("/Users/ccrowe/github/extract_twitter_favorites/keys.org") as f:
        ck,cv,sk,sv = f.read().split("\n")[:4]
        return (ck,cv,sk,sv)

consumer_key, consumer_secret, access_token, access_token_secret = get_keys()
    
import tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# Gives anything on timeline, e.g. replies
#result = api.user_timeline("Nike",count=3)
#brand = "Nike"

def get_post_data(tweet_id):
    status = api.get_status(tweet_id)
    favorite_count = status.favorite_count
    retweet_count = status.retweet_count
    created_at = status.created_at
    return (tweet_id, favorite_count, retweet_count, created_at)


tweet_id_old = "1127574455494987777"
result = get_post_data(tweet_id_old)


# The next section is about finding twitter brand pages

# from http://www.opsig.org/reso/inddb/
def insert_brand_data(brand_id):
    conn = sqlite3.connect('./usernames.db')
    conn.execute("INSERT INTO brands(brand) VALUES ('{0}')".format(brand_id))
    conn.commit()
    conn.close()

def insert_follower_data(brand, follower_id):
    conn = sqlite3.connect('./usernames.db')
    conn.execute("INSERT INTO follower(brand, followerId) VALUES ('{0}', '{1}')".format(brand, follower_id))
    conn.commit()
    conn.close()
    
def get_brand_data():
    conn = sqlite3.connect('./usernames.db')
    cursor = conn.execute("select brand from brands")
    l = []
    for row in cursor:
        l.append(row[0])
    conn.close()
    return l
    
industries = list(map(lambda x: x.split("\t")[1],
                      open("./industries.txt","r").read().split("\n")[:-1]
))
existing = get_brand_data()
for industry in industries:
    if industry in existing:
        continue # skip if we have already processed the industry
    found = api.search(industry)
    for tweet in found:
        author = tweet.author.screen_name
        print(author)
        insert_brand_data(author)
        print("processed")

import sqlite3
def create_follower_table():
    conn = sqlite3.connect('./usernames.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE followers
             (brand text, followerId integer)''')

def create_brand_table():
    conn = sqlite3.connect('./usernames.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE brands
             (brand text)''')

def create_username_table():
    conn = sqlite3.connect('./usernames.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE usernames
             (brand text, tweetId integer, favoriteUsername text, retweetUsername text)''')

def insert_username_data(brand_id, tweet_id, favorite_username, retweet_username):
    conn = sqlite3.connect('./usernames.db')
    c = conn.cursor()
    c.execute("INSERT INTO usernames VALUES ({0},{1},{2},{3})".format(brand_id, tweet_id, favorite_username, retweet_username))
    conn.commit()
    conn.close()

def delete_brand(to_remove):
    conn = sqlite3.connect('./usernames.db')
    cursor = conn.execute("delete from brands where brand = '{0}'".format(to_remove))
    conn.commit()
    conn.close()
    
# Look into api.followers
# followers_ids
# get_user
def get_user(name):
    try:
        return api.get_user(name)
    except Exception as e:
        print(str(e))
        return None

def remove_non_brands(): # We end up with around 400 brand pages, from 27k usernames
    existing = get_brand_data()
    for brand in existing: 
        user = get_user(brand)
        if user:
            follower_ratio = user.followers_count / max(1, user.friends_count)
            if follower_ratio < 5 and user.followers_count > 300:
                delete_brand(brand) # deletes from database
        else:
            delete_brand(brand)
                

# followers_count
# friends_count
# statuses_count
# friends are those they are following, followers are those following.
# we want followers / friends > 5

result = api.followers_ids(brand)
insert_follower_data

