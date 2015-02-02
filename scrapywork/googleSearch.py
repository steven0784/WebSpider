import requests
from bs4 import BeautifulSoup as bs
import re, urllib
import scrapy
from urlparse import urlparse
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
import mechanize
import json
num_queries = 10
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent','chrome')]
url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&num=100&%s' \
             % ("q=nytimes%20search%20middleeast")


htmltext = urllib.urlopen(url).read()
jsfile = json.loads(htmltext)
#print htmltext

if jsfile['responseData']:
    for result in jsfile['responseData']['results']:
        allkeys = result.keys()
        for item in allkeys:
            if 'url' in item.lower():
                print(result.get(item))

