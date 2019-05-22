import requests
import re
import uuid
import os
from bs4 import BeautifulSoup

def getImageLinksInSearchPage(searchPageURL):
    res_imageLinks = []

    response = requests.get(searchPageURL)
    soup = BeautifulSoup(response.text,'lxml')
        
    contentElem = soup.find("div", attrs={"class": "content"})
    postlistElem = contentElem.find("ul", attrs={"id": "post-list-posts"})
    if (postlistElem == None):
        return None
    postlistElems = postlistElem.find_all("li")
    for post in postlistElems:
        #determine if the default image is down-sized
        largeimgElem = post.find("a", attrs={"class": "directlink largeimg"})

        #acquire link
        if (largeimgElem == None):
            thumbnailElem = post.find("a", attrs={"class": "thumb"})
            postPageURL = "https://yande.re/" + thumbnailElem["href"][1:]
            res_imageLinks.append(getImageLinks(postPageURL))
        else:
            res_imageLinks.append(largeimgElem["href"])
    return res_imageLinks


def getImageLinks(postPageURL):
    response = requests.get(postPageURL)
    soup = BeautifulSoup(response.text,'lxml')

    #determine if the default image is down-sized
    downsizealert_tag = soup.find("div", attrs={"class": "status-notice", "style id": "resized_notice"})
    is_downsized = downsizealert_tag != None

    #acquire image url
    res_imageLink = ""
    if (is_downsized):
        alertElem = downsizealert_tag.find("a", attrs={"class": "highres-show"})
        res_imageLink = alertElem["href"]
    else:
        contentElem = soup.find("div", attrs={"class": "content", "id": "right-col"})
        imgElem = contentElem.find("img")
        res_imageLink = imgElem["src"]

    return res_imageLink     


# Support the website: yande.re @ May 22, 2019
SEARCH_TAG = "girls_und_panzer"
MAX_PAGE_INDEX = 10000 # Crawler can detect the max

print("Analyzing contents")
imageLinks = []
for pageIdx in range(1, MAX_PAGE_INDEX + 1):
    print("page"+str(pageIdx))
    links = getImageLinksInSearchPage("https://yande.re/post?page={0}&tags={1}".format(pageIdx, SEARCH_TAG))
    if (links == None):
        break
    imageLinks.extend(links)
print("got {0} image links!".format(len(imageLinks)))

i=0
for imageLink in imageLinks:
    print("{0}/{1}: {2}".format(i, len(imageLinks), imageLink))
    i=i+1
    r = requests.get(imageLink)
    gabage, imageLinkExt = os.path.splitext(imageLink)
    with open("./picture/yande.re/"+SEARCH_TAG+"/"+str(uuid.uuid4())+imageLinkExt,'wb') as file:
        file.write(r.content)
