import requests
import re
import uuid
import os
from bs4 import BeautifulSoup

def getImageLinks(tag, maxPageIndex):
    resImageLinks = []
    for pageIndex in range(1, maxPageIndex + 1):
        print('http://anime.reactor.cc/tag/{0}/{1}'.format(tag, pageIndex))
        response = requests.get('http://anime.reactor.cc/tag/{0}/{1}'.format(tag, pageIndex))
        soup = BeautifulSoup(response.text,'lxml')

        #extract post conatiner and its contents
        posts = soup.findAll("div", attrs={"class": "postContainer"})
        for post in posts:
            images = post.findAll("div", attrs={"class": "image"})
            for image in images:
                imageLink = image.find("img")
                if (imageLink == None):
                    imageLink = image.find("a", attrs={"class": "video_gif_source"})
                    if (imageLink == None):
                        pass
                    else:
                        resImageLinks.append(imageLink["href"])
                else:
                    resImageLinks.append(imageLink["src"])
    return resImageLinks            

# Support the website: anime.reactor.cc @ May 22, 2019
SEARCH_TAG = "Girls+und+Panzer"
MAX_INDEX_SEARCH_PAGES = 538

imageLinks = getImageLinks(SEARCH_TAG, MAX_INDEX_SEARCH_PAGES)
print("Got {0} image links!".format(len(imageLinks)))

i=0
for imageLink in imageLinks:
    print("{0}/{1}: {2}".format(i, len(imageLinks), imageLink))
    i=i+1
    r = requests.get(imageLink)
    gabage, imageLinkExt = os.path.splitext(imageLink)
    with open("./picture/anime.reactor.cc/"+str(uuid.uuid4())+imageLinkExt,'wb') as file:
        file.write(r.content)
