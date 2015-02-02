from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Session, Site
from .forms import *


class TestViews(TestCase):

    def setup(self):
        pass

    def testIndexStatusCode(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def testAboutStatusCode(self):
        client = Client()
        response = client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def testLoginStatusCode(self):
        client = Client()
        response = client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def testRegisterStatusCode(self):
        client = Client()
        response = client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def testAddSessionEmpty(self):
        client = Client()
        User.objects.create_user("test", "test@tester.ca", "pass")
        client.login(username="test", password="pass")
        response = client.get('/addsession/')
        self.assertEqual(response.context['sessionID'], 1)
        session = Session.objects.get(id=1)
        self.assertEqual(response.context['mysession'], session)

    def testAddSessionOne(self):
        client = Client()
        User.objects.create_user("test2", "test2@tester.ca", "pass")
        client.login(username="test2", password="pass")
        client.get('/addsession/')

        response = client.get('/addsession/')
        self.assertEqual(response.context['sessionID'], 2)
        session = Session.objects.get(id=2)
        self.assertEqual(response.context['mysession'], session)

    def testAddSessionMany(self):
        client = Client()
        User.objects.create_user("test3", "test3@tester.ca", "pass")
        client.login(username="test3", password="pass")

        response = client.get('/addsession/')
        self.assertEqual(response.context['sessionID'], 1)
        session = Session.objects.get(id=1)
        self.assertEqual(response.context['mysession'], session)

        response = client.get('/addsession/')
        self.assertEqual(response.context['sessionID'], 2)
        session = Session.objects.get(id=2)
        self.assertEqual(response.context['mysession'], session)

        response = client.get('/addsession/')
        self.assertEqual(response.context['sessionID'], 3)
        session = Session.objects.get(id=3)
        self.assertEqual(response.context['mysession'], session)

        response = client.get('/addsession/')
        self.assertEqual(response.context['sessionID'], 4)
        session = Session.objects.get(id=4)
        self.assertEqual(response.context['mysession'], session)

    def testAddSourceEmpty(self):
        client = Client()
        user = User.objects.create_user("test4", "test4@tester.ca", "pass")
        client.login(username="test4", password="pass")

        client.get('/addsession/')
        session = Session.objects.get(id=1)
        site = Site(name = "Test Site", url="http://www.test.com")
        site.save()
        session.sources.add(site)
        sessions = Session.objects.filter(user=user)

        self.assertTrue(Session.objects.get(id=1))
        self.assertTrue(session in sessions)
        self.assertTrue(site in session.sources.all())

    def testAddSourceOne(self):
        client = Client()
        user = User.objects.create_user("test4", "test4@tester.ca", "pass")
        client.login(username="test4", password="pass")

        client.get('/addsession/')
        session = Session.objects.get(id=1)
        site = Site(name = "Test Site", url="http://www.test.com")
        site.save()
        session.sources.add(site)

        site2 = Site(name= "Test Site2", url="http://www.test2.com")
        site2.save()
        session.sources.add(site2)
        sessions = Session.objects.filter(user=user)

        self.assertTrue(Session.objects.get(id=1))
        self.assertTrue(session in sessions)
        self.assertTrue(site2 in session.sources.all())

    def testAddSourceMany(self):
        client = Client()
        user = User.objects.create_user("test4", "test4@tester.ca", "pass")
        client.login(username="test4", password="pass")

        client.get('/addsession/')
        session = Session.objects.get(id=1)
        site = Site(name = "Test Site", url="http://www.test.com")
        site.save()
        session.sources.add(site)

        site2 = Site(name= "Test Site2", url="http://www.test2.com")
        site2.save()
        session.sources.add(site2)
        sessions = Session.objects.filter(user=user)

        self.assertTrue(Session.objects.get(id=1))
        self.assertTrue(session in sessions)
        self.assertTrue(site2 in session.sources.all())

        site3 = Site(name= "Test Site3", url="http://www.test4.com")
        site4 = Site(name= "Test Site4", url="http://www.test5.com")
        site5 = Site(name= "Test Site5", url="http://www.test6.com")
        site6 = Site(name= "Test Site6", url="http://www.test7.com")
        site3.save()
        site4.save()
        site5.save()
        site6.save()
        session.sources.add(site3)
        session.sources.add(site4)
        session.sources.add(site5)
        session.sources.add(site6)

        self.assertTrue(site3 in session.sources.all())
        self.assertTrue(site4 in session.sources.all())
        self.assertTrue(site5 in session.sources.all())
        self.assertTrue(site6 in session.sources.all())

    def testAddMonitorEmpty(self):
        client = Client()
        user = User.objects.create_user("test4", "test4@tester.ca", "pass")
        client.login(username="test4", password="pass")

        client.get('/addsession/')
        session = Session.objects.get(id=1)
        site = Site(name = "Monitor", url="http://www.monitor.com")
        site.save()
        session.monitors.add(site)
        sessions = Session.objects.filter(user=user)

        self.assertTrue(Session.objects.get(id=1))
        self.assertTrue(session in sessions)
        self.assertTrue(site in session.monitors.all())

    def testAddMonitorOne(self):
        client = Client()
        user = User.objects.create_user("test4", "test4@tester.ca", "pass")
        client.login(username="test4", password="pass")

        client.get('/addsession/')
        session = Session.objects.get(id=1)
        site = Site(name = "Test Site", url="http://www.test.com")
        site.save()
        session.monitors.add(site)

        site2 = Site(name= "Test Site2", url="http://www.test2.com")
        site2.save()
        session.monitors.add(site2)
        sessions = Session.objects.filter(user=user)

        self.assertTrue(Session.objects.get(id=1))
        self.assertTrue(session in sessions)
        self.assertTrue(site2 in session.monitors.all())

    def testAddMonitorMany(self):
        client = Client()
        user = User.objects.create_user("test4", "test4@tester.ca", "pass")
        client.login(username="test4", password="pass")

        client.get('/addsession/')
        session = Session.objects.get(id=1)
        site = Site(name = "Test Site", url="http://www.test.com")
        site.save()
        session.monitors.add(site)

        site2 = Site(name= "Test Site2", url="http://www.test2.com")
        site2.save()
        session.monitors.add(site2)
        sessions = Session.objects.filter(user=user)

        self.assertTrue(Session.objects.get(id=1))
        self.assertTrue(session in sessions)
        self.assertTrue(site2 in session.monitors.all())

        site3 = Site(name= "Test Site3", url="http://www.test4.com")
        site4 = Site(name= "Test Site4", url="http://www.test5.com")
        site5 = Site(name= "Test Site5", url="http://www.test6.com")
        site6 = Site(name= "Test Site6", url="http://www.test7.com")
        site3.save()
        site4.save()
        site5.save()
        site6.save()
        session.monitors.add(site3)
        session.monitors.add(site4)
        session.monitors.add(site5)
        session.monitors.add(site6)

        self.assertTrue(site3 in session.monitors.all())
        self.assertTrue(site4 in session.monitors.all())
        self.assertTrue(site5 in session.monitors.all())
        self.assertTrue(site6 in session.monitors.all())

    def testRegisterDuplicateUsername(self):
        client = Client()
        user = User.objects.create_user("test4", "test4@tester.ca", "pass")
        try:
            User.objects.create_user("test4", "tester@tester.ca", "pass")
            self.assertFail()
        except:
            self.assertTrue(True)


    def testRegisterDuplicateEmail(self):
        client = Client()
        user = User.objects.create_user("tester", "tester@tester.ca", "pass")
        try:
            User.object.create_user("tester2", "tester@tester.ca", "pass")
            self.assertFail()
        except:
            self.assertTrue(True)

    def testInvalidLogin(self):
        client = Client()
        self.assertFalse(client.login(username="Test", password="Testerspassword123"))

    def testLogin(self):
        client = Client()
        user = User.objects.create_user("tester", "tester@tester.ca", "pass")
        self.assertTrue(client.login(username="tester", password="pass"))