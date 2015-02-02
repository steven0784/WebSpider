from scrapy.selector import Selector
from scrapy.http import Request
import helper
import urllib

def find_category_links(url_list):
    result = []
    for url in url_list:
        list_urls = []
        if helper.check_url_exist(url):
            category_linklist = _find_category_linklist(url)
            if category_linklist != []:
                list_urls += category_linklist
        #encode list
        for link in list_urls:
            result.append(link.encode('utf-8'))
    return result

def _find_category_linklist(url):
    methodlist = ['class','role']
    keywordlist = ['nav']

    result_list = []
    for keyword in keywordlist:
        for method in methodlist:
            if result_list == []:
                result_list = _get_category_linklist(url, method, keyword)
            else:
                return result_list
    result_list.append(url)
    return result_list
            
def _get_category_linklist(url, method, keyword):
    category_list = []
    response = urllib.urlopen(url)
    htmltext = response.read()
    sel = Selector(text=htmltext)
    methodnames = sel.xpath('//div/@%s' % (method)).extract()
    keywordnamelist = []
    for content in methodnames:
        if keyword in content.encode('utf-8'):
            keywordnamelist.append(content.encode('utf-8'))
    if keywordnamelist != []:
        for name in keywordnamelist:
            keyword_div = sel.xpath('//div[@%s="%s"]' % (method, name))
            category_list = keyword_div.xpath('.//a/@href').extract()
    return category_list