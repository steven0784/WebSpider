all: clean database
	
database:
	cd WebSpider && python manage.py makemigrations
	cd WebSpider && python manage.py migrate
	cd WebSpider && python populate.py

run:
	cd WebSpider && celery -A WebSpider worker -l info & 
	cd WebSpider && python manage.py runserver

test:
	cd WebSpider && python manage.py test crawler

clean:
	cd WebSpider && rm -f db.sqlite3
	cd WebSpider && rm -rf crawler/migrations
	cd WebSpider && python manage.py makemigrations crawler
	