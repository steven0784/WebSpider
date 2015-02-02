from scrapy.selector import Selector
from nytimes.items import MainItem
from scrapy.http import Request
import helper

#method that get links or article 
def start_scrapy(response, item_list, keyword):
   linklist = _find_link(response, item_list, keyword)
   return linklist
   #articlelist = _find_article(response, linklist, keyword)
   #
   #if articlelist == []:
   #   item = MainItem()
   #   item['status'] = "None"
   #   articlelist.append(item)
   #elif linklist == []:
   #   for dictitem in articlelist:
   #      dictitem['status'] = "article site"
   #else:
   #   for dictitem in articlelist:
   #      dictitem['status'] = "link site"
   #return articlelist

def _find_link(response, items, keyword):
   sel = Selector(response)
   sites = sel.xpath('//a')
   for site in sites:
       item = MainItem()
       addrnamelist = site.xpath('./text()').extract()
       addrlinklist = site.xpath('./@href').extract()
       item['name'] = addrnamelist
       item['url'] = addrlinklist
       item['source'] = helper.find_domain_url(response.url)
       items.append(item.copy())
       #for index in range(len(addrlinklist)):
       #  if addrnamelist != []:
       #    if keyword.lower() in addrnamelist[0].encode('utf-8').lower():
       #     store_link = addrlinklist[index].encode('utf-8')
       #     if helper.check_url_duplicate(items, store_link) == -1:
       #        item['name'] = addrnamelist[index].encode('utf-8')
       #        item['url'] =  store_link
       #        items.append(item.copy())
   return items

def _find_article(response, items, keyword):
   sel = Selector(response)
   item = MainItem()
   current_url = response.url
   paragraphlist = sel.xpath('//p/text()').extract()
   if paragraphlist != []:
      for text in paragraphlist:
         if keyword.lower() in text.encode('utf-8').lower():
            indicater = helper.check_url_duplicate(items, current_url)
            if indicater == -1:
               item['url'] = current_url
               item['body'] = text.encode('utf-8')
               items.append(item.copy())
            else:
               items[index]['body'] = text.encode('utf-8')
   return items



