# coding: utf-8
from pixivpy3 import *
import json
from time import sleep
import os
import uuid

# Login to pixiv
api = PixivAPI()
api.login('YOUR MAIL ADDR', 'YOUR PASS')

START_PAGE = 1
END_PAGE = 100000 # Crawler can detect the bounds
SEARCH_METHODS = "tag"
PER_PAGE = 30
KEYWORD = "ガールズ&パンツァー"

json_result = api.search_works(KEYWORD, page=1, per_page=PER_PAGE, mode=SEARCH_METHODS)
END_PAGE = json_result.pagination.pages

for pageIdx in range(START_PAGE, END_PAGE + 1):
    json_result = api.search_works(KEYWORD, page=pageIdx, mode=SEARCH_METHODS)
    
    for illustIdx in range(0, len(json_result.response)):
        print("{0}/{1}...{2} search...".format(pageIdx*PER_PAGE+illustIdx-PER_PAGE, END_PAGE*PER_PAGE, SEARCH_METHODS))
        illust = json_result.response[illustIdx]
        
        saving_direcory_path = "./picture/pixiv/" + str(illust.user.id)
        if not os.path.exists(saving_direcory_path):
            os.mkdir(saving_direcory_path)
        
        aapi = AppPixivAPI()
        aapi.download(illust.image_urls.large, saving_direcory_path + "/")
        sleep(1)
