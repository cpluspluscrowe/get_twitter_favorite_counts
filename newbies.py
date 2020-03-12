import sqlite3

def create_newbies_table():
    conn = sqlite3.connect('./usernames.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE newbies
             (tweetId integer, username text)''')

def get_usernames(brand_id):
    conn = sqlite3.connect('./usernames.db')
    cursor = conn.execute('''
SELECT distinct users.username, media.tweetId from media
INNER JOIN tweets on tweets.tweetId = media.tweetId
INNER JOIN users on users.tweetId = tweets.tweetId 
where tweets.brandId = '{0}'
order by media.timestamp asc
'''.format(brand_id))
    l = []
    for row in cursor:
        l.append(row)
    conn.close()
    return l

def insert_newbie_data(tweet_id, username):
    conn = sqlite3.connect('./usernames.db')
    c = conn.cursor()
    c.execute("INSERT INTO newbies VALUES ({0},'{1}')".format(tweet_id, username))
    conn.commit()
    conn.close()


def fill_newbiew_db(brand):
    replace = "https://twitter.com/"
    user_tweets = get_usernames(brand)
    usernames = list(
        filter(lambda x: not "search" in x[0] and x[0],
               filter(lambda x: len(x[0].split("/")) == 1,
                      map(lambda x: (x[0].replace(replace,""), x[1]), user_tweets)
               )))
    ignore = set()
    for x in range(min(10, len(usernames) - 1)):
        username, tweet_id = usernames[x]
        ignore.add(username)
        usernames.remove((username, tweet_id))
        for username, tweet_id in usernames:
            if not username in ignore:
                insert_newbie_data(tweet_id, username)

    

    
