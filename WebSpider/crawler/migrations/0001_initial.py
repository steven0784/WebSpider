# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='crawlData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article_title', models.CharField(max_length=132, null=True, blank=True)),
                ('article_url', models.CharField(max_length=132, null=True, blank=True)),
                ('ref_link', models.CharField(max_length=132, null=True, blank=True)),
                ('excerpts', models.CharField(max_length=132, null=True, blank=True)),
                ('ref_keyword', models.CharField(max_length=132, null=True, blank=True)),
                ('in_sessionID', models.IntegerField()),
                ('in_resultID', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CrawledData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monitor', models.CharField(max_length=100)),
                ('lookingfor', models.CharField(max_length=100)),
                ('hits', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='resultLogData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sessionID', models.CharField(max_length=132, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('sessionID', models.IntegerField()),
                ('nextSessionID', models.IntegerField()),
                ('result_count', models.IntegerField(default=0)),
                ('data', models.ForeignKey(to='crawler.CrawledData', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('url', models.URLField(max_length=120)),
                ('keywords', models.CharField(max_length=120, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='session',
            name='monitors',
            field=models.ManyToManyField(related_name=b'monitor', to='crawler.Site'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='session',
            name='sources',
            field=models.ManyToManyField(related_name=b'source', to='crawler.Site'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='session',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
