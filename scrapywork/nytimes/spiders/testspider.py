import re
import os
import sys
import json
from scrapy.spider import Spider
from scrapy.selector import Selector
from nytimes.items import MainItem
from scrapy.http import Request

class MainSpider(Spider):
   name = 'testspider'
   #make_urls = DataAnalysis(["http://www.nytimes.com/"], 'goldman')
    
   start_urls = ["http://www.nytimes.com/"]
   global keyword
   keyword = "Heavy Snow"
   
   def parse(self, response):
        sel = Selector(response)
        #directory-url
        sites = sel.xpath('//a')
        count = 0
        items = []
        for site in sites:
            item = MainItem()
            addrnamelist = site.xpath('./text()').extract()
            count += len(addrnamelist)
            addrlinklist = site.xpath('./@href').extract()
            for index in range(len(addrnamelist)):
              if addrnamelist != []:
                if keyword.lower() in addrnamelist[0].encode('utf-8').lower():
                    item['name'] = addrnamelist[index].encode('utf-8')
                    link =  addrlinklist[index].encode('utf-8')
                    item['url'] = link
                    items.append(item.copy())
                    request = Request(link, callback=self.parse_content)
                    request.meta['item'] = item
                    request.meta['list'] = items
                    yield request
   def parse_content(self, response):
      item = response.meta['item']
      items = response.meta['list']
      item['body'] = response.url
      items.append(item.copy())
      return items
