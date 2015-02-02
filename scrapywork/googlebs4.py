import requests
from bs4 import BeautifulSoup as bs
import re, urllib
import scrapy
from urlparse import urlparse
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
import mechanize

##url = "http://query.nytimes.com/search/sitesearch/#/israel"
##response = urllib.urlopen(url)
##htmltext = response.read()
##print htmltext


def getGoogleLinks(link,depth):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent','chrome')]

    term = link.replace(" ","+")
    query = "http://www.google.com/search?num=100&q=" + term + "&start=" + depth
    htmltext = br.open(query).read()
    soup = bs(htmltext)
    search = soup.findAll('div', attrs={'id':'search'})
    searchtext = str(search[0])
    soup1 = bs(searchtext)
    list_items = soup1.findAll('li')

    regex = "q(?!.*q).*?&amp"
    pattern = re.compile(regex)

    results_array = []

    for li in list_items:
        soup2 = bs(str(li))
        links = soup2.findAll('a')
        source_link = links[0]
        source_url = re.findall(pattern, str(source_link))
        if len(source_url)>0:
            results_array.append(str(source_url[0].replace("q=","").replace("&amp","")))
    return results_array

##def getLinkRecursive(term, depth):
##    i=0
##    results_array = []
##    while i<depth:
##        results_array.append(getGoogleLinks(term, str(depth*100)))
##        i+=1
##    return results_array

print getGoogleLinks('nytimes search israel',"100")





















##sites = sel.xpath('//div')
##items = []
##for site in sites:
##    item = NytimesItem()
##    classcontents = site.xpath('//div/@class').extract()
##    storyclass = []
##    for i in classcontents:
##        if 'story' in i:
##                body = site.xpath('//div/@class="%s"' % (i)).extract()
##                item['body'] = body
##                items.append(item)
