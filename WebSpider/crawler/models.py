from django.db import models
from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User

# Create your models here.

class Site(models.Model):
    name = models.CharField(max_length=120)
    url = models.URLField(max_length=120)
    keywords = models.CharField(max_length=120, null = True, blank = True)
    def __unicode__(self):
        return self.name

class crawlData(models.Model):
    article_title  = models.CharField(max_length=132, null = True, blank = True)
    article_url = models.CharField(max_length=132, null = True, blank = True)
    ref_link = models.CharField(max_length=132, null = True, blank = True)
    excerpts = models.CharField(max_length=132, null = True, blank = True)
    ref_keyword = models.CharField(max_length=132, null = True, blank = True)
    in_sessionID = models.IntegerField()
    in_resultID = models.IntegerField()
    #name = title
    #link = url
    #desc = body
    #source = origin
    def __unicode__(self):
        return self.article_title
    
class resultLogData(models.Model):
    sessionID  = models.CharField(max_length=132, null = True, blank = True)
    
    def __unicode__(self):
        return self.sessionID

class CrawledData(models.Model):
    monitor = models.CharField(max_length=100)
    lookingfor = models.CharField(max_length=100)
    #owner = models.ForeignKey(User)
    hits = models.IntegerField()

    def __unicode__(self):
        return smart_unicode(self.lookingfor)

class Session(models.Model):
    user = models.ForeignKey(User)
    #jobs = models.ManyToManyField(Job)
    sources = models.ManyToManyField(Site, related_name='source')
    monitors = models.ManyToManyField(Site, related_name='monitor')
    data = models.ForeignKey(CrawledData, null=True)
    date = models.DateTimeField(auto_now_add=True)
    sessionID = models.IntegerField()
    nextSessionID = models.IntegerField()
    result_count = models.IntegerField(default=0)
    def __unicode__(self):
        return str(self.date)
    
class job(models.Model):
    pass
