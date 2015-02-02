from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WebSpider.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'crawler.views.index', name='root'),
    url(r'^(?P<sessionID>\d+)/$', 'crawler.views.index', name='index'),
    url(r'^thankyou/', 'crawler.views.thankspage', name='thanks'),
    url(r'^register/', 'crawler.views.register', name='register'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^job/','crawler.views.job', name='job'),
    url(r'^addsession/','crawler.views.addsession', name='addsession'),
    url(r'^addsource$','crawler.views.addsource', name='addsource'),
    url(r'^addsource(?P<sessionID>\d+)/$','crawler.views.addsource', name='addsources'),
    url(r'^crawling$','crawler.views.crawling', name='crawling'),
    url(r'^crawling(?P<sessionID>\d+)/$','crawler.views.crawling', name='crawling'),
    url(r'^addmonitor$','crawler.views.addmonitor', name='addmonitor'),
    url(r'^addmonitor(?P<sessionID>\d+)/$','crawler.views.addmonitor', name='addmonitor'),
    url(r'^login/$','crawler.views.user_login', name='login'),
    url(r'^about/', 'crawler.views.about', name='about'),
    url(r'^logout/$', 'crawler.views.user_logout', name='logout'),
    url(r'^invalidUser/', 'crawler.views.invalidUser', name='invalidUser'),
    url(r'^results$','crawler.views.results', name='results'),
    url(r'^results(?P<sessionID>\d+)/$','crawler.views.results', name='results'),
    url(r'^summary$','crawler.views.summary', name='summary'),
    url(r'^summary(?P<sessionID>\d+)/$','crawler.views.summary', name='summary'),
    url(r'^removesource$','crawler.views.removesource', name='removesource'),
    url(r'^removesource(?P<sessionID>\d+)(?P<source_name>.+)/$','crawler.views.removesource', name='removesource'),
    url(r'^removemonitor$','crawler.views.removemonitor', name='removemonitor'),
    url(r'^removemonitor(?P<sessionID>\d+)(?P<monitor_name>.+)/$','crawler.views.removemonitor', name='removemonitor'),
    url(r'^removesession$','crawler.views.removesession', name='removesession'),
    url(r'^removesession(?P<sessionID>\d+)/$','crawler.views.removesession', name='removesession'),
    url(r'^addexistingsource$','crawler.views.addexistingsource', name='addexistingsource'),
    url(r'^addexistingsource(?P<sessionID>\d+)(?P<source_name>.+)/$','crawler.views.addexistingsource', name='addexistingsource'),
    url(r'^addexistingmonitor$','crawler.views.addexistingmonitor', name='addexistingmonitor'),
    url(r'^addexistingmonitor(?P<sessionID>\d+)(?P<monitor_name>.+)/$','crawler.views.addexistingmonitor', name='addexistingmonitor'),
)
#this part is only for static folder for debug
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


