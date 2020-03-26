
import urllib
from lxml.html import parse

import urllib.request


screen_name = "alien_merchant"
status_id = "934338104797945856"


from bs4 import BeautifulSoup
import requests




# =============================================================================
url = "http://twitter.com/alien_merchant/status/934338104797945856"
# 
# html = requests.get(url).content
# bsObj = BeautifulSoup(html, 'lxml')
# 
# links = bsObj.find_all('a', recursive=True)
# finalLinks = set()
# interactors = set()
# for link in links:
#     if "data-user-id" in link.attrs:
#         interactors.add(link.attrs['href'])
#         
# print(len(interactors))
# for x in interactors:
#     print(x)
# =============================================================================
    

import urllib
from lxml.html import parse

import urllib.request
#returns list(retweet users),list(favorite users) for a given screen_name and status_id
url = urllib.request.urlopen('https://twitter.com/' + screen_name + '/status/' + status_id)
root = parse(url).getroot()

num_rts = 0
num_favs = 0
rt_users = []
fav_users = []

for ul in root.find_class('stats'):
    for li in ul.cssselect('li'):

        cls_name = li.attrib['class']

        if cls_name.find('retweet') >= 0:
            num_rts = int(li.cssselect('a')[0].attrib['data-tweet-stat-count'])

        elif cls_name.find('favorit') >= 0:
            num_favs = int(li.cssselect('a')[0].attrib['data-tweet-stat-count'])

        elif cls_name.find('avatar') >= 0 or cls_name.find('face-pile') >= 0:#else face-plant

            for users in li.cssselect('a'):
                #apparently, favs are listed before retweets, but the retweet summary's listed before the fav summary
                #if in doubt you can take the difference of returned uids here with retweet uids from the official api
                if num_favs > 0:#num_rt > 0:
                    #num_rts -= 1
                    num_favs -= 1
                    #rt_users.append(users.attrib['data-user-id'])
                    fav_users.append(users.attrib['data-user-id'])
                else:                        
                    #fav_users.append(users.attrib['data-user-id'])
                    rt_users.append(users.attrib['data-user-id'])


#example
if __name__ == '__main__':
    print(get_twitter_user_rts_and_favs('Nike', '1225203298443153409'))


