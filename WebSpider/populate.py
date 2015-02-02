import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebSpider.settings')

import django
django.setup()

from crawler.models import User, CrawledData #Category, Page


def populate():
    add_superuser()
    p = User.objects.create_user('user', 'user@gmail.com', 'pass')
    # Print out what we have added to the user.
    for c in User.objects.all():
        print "Add %s as User" %(str(c))
    add_crawled_data()


def add_superuser():
    p = User.objects.create_superuser('admin', 'admin@email.com', 'pass')
    return p
# Start execution here!

def add_crawled_data():
    CrawledData.objects.create(monitor="http://www.nytimes.com", lookingfor="http://www.haaretz.com", hits=150)
    CrawledData.objects.create(monitor="http://www.cnn.com", lookingfor="http://www.haaretz.com", hits=120)
    CrawledData.objects.create(monitor="http://www.cnn.com", lookingfor="http://www.jpost.com", hits=85)
    CrawledData.objects.create(monitor="http://www.nytimes.com", lookingfor="http://www.jpost.com", hits=54)

if __name__ == '__main__':
    print "Starting WebCrawler population script..."
    populate()
