
# Need to login in order to get favorite information
import sqlite3
import time
import os
import sys
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
#https://twitter.com/barkbox

login_password = open("./password.org").read().split("\n")[0]

def login_to_twitter():
    def setupChromeDriver():
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_driver_location = "/Users/ccrowe/github/extract_twitter_favorites/chromedriver"
        driver = webdriver.Chrome(chrome_driver_location, chrome_options=chrome_options)
        return driver
    driver = setupChromeDriver()
    def login(driver):
        url = "https://twitter.com/login"
        driver.get(url)
        time.sleep(3)
        username = driver.find_elements_by_name("session[username_or_email]")
        username[0].send_keys("cpluspluscrowe")
        time.sleep(2)
        password = driver.find_elements_by_name("session[password]")
        password[0].send_keys(login_password)
        time.sleep(2)
        submit = driver.find_element_by_xpath("//span[text()='Log in']")
        submit.click()
        time.sleep(1)
        return driver
    return login(driver)

# Now get likes

def get_usernames(url, text):
    driver.get(url)
    time.sleep(3)
    height = driver.execute_script("return document.body.scrollHeight;")
    collected_usernames = set()
    for pixel in range(1, height, 20):
        usernames = set(driver.execute_script('''var arr = [], l = document.links;for(var i=0; i<l.length; i++){  arr.push(l[i].href);};return arr;'''))
        collected_usernames = collected_usernames.union(usernames)
        driver.execute_script("scroll({0}, {1});".format(pixel, pixel - 1))
    return collected_usernames

def get_likes(url):
    return get_usernames(url + "/likes", "Liked by")

def get_retweets(url):
    return get_usernames(url + "/retweets", "Retweeted by")

def get_data(url):
#    driver.get(url)
#    time.sleep(2)
    likes = get_likes(url)
    retweets = get_retweets(url)
    to_return = (likes, retweets)
    return to_return

#url = "https://twitter.com/PLAYRgg/status/1230628361984233474"
#likes, retweets = get_data(url)


# get tweets from the brand's page

# ---- There are certain signs that you are too cool for Python
import sys
sys.setrecursionlimit(100000)
# ----

def get_tweet_ids(url, old_height, count, collected_tweet_ids):
    if old_height == 0:
        driver.get(url)
        time.sleep(2)
    driver.execute_script("window.scrollBy(0,500)")
    height = driver.execute_script("return document.body.scrollHeight;")
    old_id_count = len(collected_tweet_ids)
    # role = link
    elements = driver.find_elements_by_xpath("//div[@data-testid='tweet']//a[@role='link']")
    for element in elements:
        try:
            tweet_id = element.get_attribute("href").split("/")[-1:][0]
            collected_tweet_ids.add(tweet_id)
        except:
            print("error getting tweet id")
    print(len(collected_tweet_ids))
    new_id_count = len(collected_tweet_ids)
    print("Count: {0}, old_id_count: {1}, new_id_count: {2}".format(count,old_id_count,new_id_count))
    if count > 100 or new_id_count == 0:
        print("Done Counting!: {0}".format(new_id_count))
        return list(collected_tweet_ids)
    elif old_id_count == new_id_count:
        new_count = count + 1
        return get_tweet_ids(url, height, new_count, collected_tweet_ids)
    elif new_id_count > old_id_count:
        return get_tweet_ids(url, height, 1, collected_tweet_ids)
    else:
        raise Exception("Else reached, should not happen")
 

def create_tweet_id_table():
    conn = sqlite3.connect('./usernames.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE tweets
             (brandId text, tweetId text)''')

def insert_tweet_id(brand_id, tweet_id):
    conn = sqlite3.connect('./usernames.db')
    c = conn.cursor()
    c.execute("INSERT INTO tweets(brandId, tweetId) VALUES ('{0}','{1}')".format(brand_id, tweet_id))
    conn.commit()
    conn.close()

def delete_tweet_id(brand_id):
    conn = sqlite3.connect('./usernames.db')
    c = conn.cursor()
    c.execute("delete from brands where brand = '{0}'".format(brand_id))
    conn.commit()
    conn.close()
    
def get_and_store_brand_tweet_ids(brand):
    url = "https://twitter.com/{0}".format(brand)
    tweet_ids = get_tweet_ids(url, 0, 0, set())
    if len(tweet_ids) == 0:
        delete_tweet_id(brand)
        return
    for tweet_id in tweet_ids:
        insert_tweet_id(brand, tweet_id)

def get_brand_data():
    conn = sqlite3.connect('./usernames.db')
    cursor = conn.execute("select brand from brands")
    l = []
    for row in cursor:
        l.append(row[0])
    conn.close()
    return l

def get_searched_twitter_pages():
    conn = sqlite3.connect('./usernames.db')
    cursor = conn.execute("select brandId from tweets")
    l = []
    for row in cursor:
        l.append(row[0])
    conn.close()
    return l

driver = login_to_twitter()
#already_searched = get_searched_twitter_pages()
#existing = get_brand_data()
#for brand in existing:
#    if not brand in already_searched:
#        get_and_store_brand_tweet_ids(brand)


def get_tweet_ids():
    conn = sqlite3.connect('./usernames.db')
    cursor = conn.execute("select brandId, tweetId from tweets")
    l = []
    for row in cursor:
        l.append(row)
    conn.close()
    return l

def create_persons_table():
    conn = sqlite3.connect('./usernames.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE users
             (tweetId integer, username text, favorite integer, retweet integer)''')

def insert_person_id(tweet_id, username, is_favorite, is_retweet):
    conn = sqlite3.connect('./usernames.db')
    c = conn.cursor()
    c.execute("INSERT INTO users(tweetId, username, favorite, retweet) VALUES ('{0}','{1}','{2}','{3}')".format(tweet_id, username, is_favorite, is_retweet))
    conn.commit()
    conn.close()

def get_already_parsed_tweets():
    conn = sqlite3.connect('./usernames.db')
    cursor = conn.execute("select tweetId from users")
    l = []
    for row in cursor:
        l.append(str(row[0]))
    conn.close()
    return l

tweet_ids = get_tweet_ids()
filtered = list(filter(lambda x: x[0] == "GigsStem", tweet_ids))

extracted = get_already_parsed_tweets()

for brand,tweet_id in filtered:#tweet_ids:
    if not tweet_id.isnumeric() or tweet_id in extracted:
        print(tweet_id in extracted)
        continue
    url = "https://twitter.com/{0}/status/{1}".format(brand,tweet_id)
    likes, retweets = get_data(url)
    print("Likes: {0}".format(likes))
    print("Retweets: {0}".format(retweets))
    if len(likes) == 0 and len(retweets) == 0:
        time.sleep(2)
    print()
    for like in likes:
        insert_person_id(tweet_id, like, 1, 0)
    for retweet in retweets:
        insert_person_id(tweet_id, retweet, 0, 1)
    


        

#SELECT distinct tweets.brandId, users.username, media.tweetId, media.timestamp from media
#INNER JOIN tweets on tweets.tweetId = media.tweetId
#INNER JOIN users on users.tweetId = tweets.tweetId 
#where media.hasText = "True" order by media.timestamp asc


