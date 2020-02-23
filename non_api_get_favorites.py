
# Need to login in order to get favorite information
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
    time.sleep(1)
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
    driver.get(url)
    likes = get_likes(url)
    retweets = get_retweets(url)
    to_return = (likes, retweets)
    print(len(to_return[0]), len(to_return[1]))
    return to_return

#url = "https://twitter.com/PLAYRgg/status/1230628361984233474"
#likes, retweets = get_data(url)


# get tweets from the brand's page
driver = login_to_twitter()
url = "https://twitter.com/rishqo"

# ---- There are certain signs that you are too cool for Python
import sys
sys.setrecursionlimit(100000)
# ----

def get_tweet_ids(url, old_height, count, collected_tweet_ids):
    if old_height == 0:
        driver.get(url)
        time.sleep(1)
    driver.execute_script("window.scrollBy(0,2000)")
    time.sleep(0.3)
    height = driver.execute_script("return document.body.scrollHeight;")
    elements = driver.find_elements_by_xpath("//div[@data-testid='tweet']//a[contains(@href,'/{0}/status/')]".format(brand))
    for element in elements:
        tweet_id = element.get_attribute("href").split("/")[-1:][0]
        collected_tweet_ids.append(tweet_id)
    print(len(collected_tweet_ids))
    if len(collected_tweet_ids) > 50:
        return collected_tweet_ids
    if height == old_height and count > 5:
        return collected_tweet_ids
    if height == old_height and count < 5:
        new_count = count + 1
        return get_tweet_ids(url, height, new_count, collected_tweet_ids)
    else:
        return get_tweet_ids(url, height, 1, collected_tweet_ids)

import sqlite3
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

def get_and_store_brand_tweet_ids(brand):
    url = "https://twitter.com/{0}".format(brand)
    tweet_ids = get_tweet_ids(url, 0, 0, [])
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

existing = get_brand_data()
for brand in existing:
    get_and_store_brand_tweet_ids(brand)
