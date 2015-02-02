#import scrapy
#from scrapy.spider import BaseSpider
#from mybot.items import crawlDataItem
#from django.db import models
#from crawler.models import Site,crawlData
#class ExampleSpider(BaseSpider):
#    name = "example"
#    input_list = Site.objects.all()
#    url_list = []
#    for item in input_list:
#        url_list.append(item.url)
#    start_urls = url_list
#
#    def parse(self, response):
#        for site in response.xpath('//ul/li'):
#            status = 0;
#            flag = 0;
#            #get crawlDataItem models as a dictionary called item
#            item = crawlDataItem()
#            #set the value for the key of origin
#            item['origin'] = response.url
#            #get a list of links text from every a-link
#            link_name = site.xpath('a/text()').extract()
#            if link_name != []:
#                #convert scraped link as string format
#                #and strip the /n/t/r characters and spaces
#                str_link = link_name[0].encode("utf-8").strip()
#                if str_link == "" :
#                    status = 1
#                else:
#                    #store string type link into title's value
#                    item['title'] = str_link
#            else:
#                status = 1;
#            #get extract text into desc's value
#            item['desc'] = site.xpath('text()').extract()
#            link_urls = site.xpath('a/@href').extract()
#            if link_urls != []:
#                str_urls = link_urls[0].encode("utf-8").strip()
#                #if the url doesn't start as http
#                if str_urls[:3]!="htt":
#                    link_to_store = response.url+"/"
#                else:
#                    link_to_store = ""
#                for link in str_urls:
#                    if link.strip():
#                        if link[:3]!="../":
#                            link_to_store += link.encode("utf-8").strip()
#                        else:
#                            link_to_store += link[3:]
#                if link_to_store.strip():
#                    item['link'] = link_to_store
#                    #if no link text exist
#                    if status == 1:
#                        item['title'] = link_to_store
#                        
#                    data = crawlData.objects.all()
#                    for stuff in data:
#                        if stuff.origin == item['origin'] and stuff.link == item['link']:
#                            flag = 1;
#                    if flag == 0:
#                        yield item
#            