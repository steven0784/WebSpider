# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem

class MybotPipeline(object):
    def process_item(self, item, spider):
        item.save()
        #spider.log('We are saving via pipleline: %s' % item['article_title'])
        #print('We are saving via pipleline: %s' % item['article_title'])
        return item
       
        #raise DropItem("Duplicate item found: %s" % item)

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['link'][0] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['link'][0])
            return item

class CleanSpace(object):
    def process_item(self, item, spider):
        try:
            if item['excerpts']:
                item['excerpts'] = item['excerpts'].strip(' \t\n\r')
            return item
        except Exception, e:
            return item