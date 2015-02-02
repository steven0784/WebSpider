from django.contrib import admin

# Register your models here.
from .models import Site, Session
from .models import crawlData, CrawledData

admin.site.register(crawlData)
admin.site.register(CrawledData)
admin.site.register(Site)
admin.site.register(Session)