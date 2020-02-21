
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

password = open("./password.org").read().split("\n")[0]

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
        time.sleep(6)
        username = driver.find_elements_by_name("session[username_or_email]")
        username[0].send_keys("cpluspluscrowe")
        time.sleep(2)
        password = driver.find_elements_by_name("session[password]")
        password[0].send_keys(password)
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

url = "https://twitter.com/PLAYRgg/status/1230628361984233474"
likes, retweets = get_data(url)
        
