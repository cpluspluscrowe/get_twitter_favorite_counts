
# Need to login in order to get favorite information

goal_post_url = "https://twitter.com/saucony/status/1229450434000982022"
chrome_driver_location = "/Users/ccrowe/github/extract_twitter_favorites/chromedriver"

import os
import sys
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options


def setupChromeDriver():
    # setup chrome driver
    chrome_options = Options()
#    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_driver_location, chrome_options=chrome_options)
    return driver

driver = setupChromeDriver()



# Now work on logging into Twitter
url = "https://twitter.com/login"
driver.get(url)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

driver = webdriver.Chrome(executable_path = r'D:/Automation/chromedriver.exe')
driver.get("https://twitter.com/login")

# To get UNO Access for gathering Twitter data

username = driver.find_elements_by_name("session[username_or_email]")
username[0].send_keys("cpluspluscrowe")

password = driver.find_elements_by_name("session[password]")
password[0].send_keys("rickroll")


submit = driver.find_element_by_xpath("//span[text()='Log in']")
submit.click()


# Now get likes

def get_usernames(url, text):
    driver.get(url)
    time.sleep(1)
    element_to_hover_over = driver.find_elements_by_xpath("//*[contains(text(), '{0}')/span]".format(text))[0]
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.click_and_hold()    
    from selenium.webdriver.common.keys import Keys
    hover.send_keys(Keys.END)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    usernames = driver.execute_script('''var arr = [], l = document.links;for(var i=0; i<l.length; i++){  arr.push(l[i].href);};return arr;''')
    print(len(usernames))
    return usernames

def scroll_page():
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        traffic_path = driver.find_elements_by_css_selector("a[aria-label='View Tweet activity']")
        path.extend([traffic.get_attribute('href') for traffic in traffic_path])
        driver.execute_script("window.scrollTo(0, {})".format(last_height+500))
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
            break
url = "https://twitter.com/saucony/status/1229450434000982022"
driver.get(url)
likes_url = "https://twitter.com/saucony/status/1229450434000982022/likes"
retweets_url = "https://twitter.com/saucony/status/1229450434000982022/retweets"
usernames1 = get_usernames(likes_url, "Liked by")
usernames2 = get_usernames(retweets_url, "Retweeted by")
print(len(usernames1))
print(len(usernames2))
all_usernames = usernames1 + usernames2

def getPageNumber(driver, current_page=-1):
    
        

    if current_page == pageNumber:
        time.sleep(0.0001)
        return getPageNumber(driver, current_page)
    return pageNumber


#document.getElementsByTagName("a").length
#        '''var pageNumber = document.getElementsByClassName("pagination-info").item(0).innerHTML;return pageNumber;''').replace(
#        "Page <strong>", "").split("</strong>")[0].replace(" ", ""))
