
# Digest data by brand

#1. take brand
#2. get tweets on brand page
#3. get media on brand page
#4. get usernames on page
#5. get uniques on brand page
import sqlite3
import os
import sys
scriptpath = "./"
sys.path.append(os.path.abspath(scriptpath))

def create_completed_table():
    conn = sqlite3.connect('./usernames.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE completed
             (brandId text)''')

def insert_completed_brand_id(brand_id):
    conn = sqlite3.connect('./usernames.db')
    c = conn.cursor()
    c.execute("INSERT INTO completed(brandId) VALUES ('{0}')".format(brand_id))
    conn.commit()
    conn.close()

def get_completed():
    conn = sqlite3.connect('./usernames.db')
    cursor = conn.execute("select distinct brandId from completed")
    l = []
    for row in cursor:
        l.append(row[0])
    conn.close()
    return l

# Do the import
from py_api import get_brand_data
#brands = get_brand_data()
#1
completed = get_completed()
brands = get_brand_data()
for brand in brands:
    if not brand in completed:
        print("Brand: ",brand)
        #2
        from non_api_get_favorites import get_and_store_brand_tweet_ids
        get_and_store_brand_tweet_ids(brand)
        #3
        from py_api import insert_media
        insert_media(brand)
        #4
        from non_api_get_favorites import get_retweet_favorite_usernames
        get_retweet_favorite_usernames(brand)
        #5
        from newbies import fill_newbiew_db
        fill_newbiew_db(brand)
        #6 record complete
        insert_completed_brand_id(brand)
