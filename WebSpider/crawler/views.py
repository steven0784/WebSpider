from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect
# Create your views here.
from django.contrib import messages

# Create your views here.
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .forms import UserForm, AddSiteForm

from .models import Session, User, Site
from .models import crawlData
from .models import CrawledData, resultLogData
from itertools import chain
import subprocess
import urllib
import re
import datetime
from .tasks import crawl_domain
l=[]

def index(request, sessionID=0):
    if request.user.is_authenticated():
        sessions = Session.objects.filter(user=request.user)
        if not sessions:
            return render(request, "index.html", {"sessions" : sessions, "sessionID" : int(sessionID)})
        else:
            sessionID = int(sessionID)
            if sessionID == 0:
                session = sessions[0]
                sessionID = session.sessionID
            else:
                session = sessions.get(sessionID=sessionID)
            sources = session.sources.all()
            monitor = session.monitors.all()
            allLog = resultLogData.objects.all()
            p = []
            for i in allLog:
                p.append(int(i.sessionID))
            return render(request, "index.html", {"sessions" : sessions, "sessionID" : int(sessionID), "mysession" : session, "sources" : sources, "monitors" : monitor, "p" : p})
    else:
        return render(request, "index.html", None)

@login_required
def addsession(request):
    sessions = Session.objects.filter(user=request.user)
    if len(sessions) == 0:
        sessionID = 1
    else:
        sessionID = sessions[0].nextSessionID
    session = Session(user=request.user, date=datetime.datetime.now(), sessionID=sessionID, nextSessionID=sessionID)
    session.save()
    sessions = Session.objects.filter(user=request.user)
    for session in sessions:
        session.nextSessionID += 1
        session.save()
    return HttpResponseRedirect('/'+str(sessionID))

@login_required
def removesession(request, sessionID):
    sessions = Session.objects.filter(user=request.user)
    session = sessions.get(sessionID=sessionID)
    session.delete()
    sessions = Session.objects.filter(user=request.user)
    if len(sessions) == 0:
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/'+str(sessions[0].sessionID))

@login_required
def addsource(request, sessionID):
    sessionID = int(sessionID)
    sessions = Session.objects.filter(user=request.user)
    session = sessions.get(sessionID=sessionID)
    if request.method == 'POST':
        form = AddSiteForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            url = form.cleaned_data['url']
            keywords = form.cleaned_data['keywords']
            try:
                site = Site.objects.get(name=name)
                if not(site in session.sources.all()):
                    session.sources.add(site)
            except Site.DoesNotExist:
                site = Site(name=name, url=url, keywords=keywords)
                site.save()
                session.sources.add(site)
            return HttpResponseRedirect('/'+str(sessionID))
        else:
            return render(request, "siteList.html", {'form': form, 'sessions': sessions, 'session' : session, 'sessionID': sessionID, 'source': True})
    else:
        form = AddSiteForm()
        return render(request, "siteList.html", {'form': form, 'sessions': sessions, 'session' : session, 'sessionID': sessionID, 'source': True})

@login_required
def addexistingsource(request, sessionID, source_name):
    sessionID = int(sessionID)
    sessions = Session.objects.filter(user=request.user)
    session = sessions.get(sessionID=sessionID)
    source = Site.objects.get(name=source_name)
    session.sources.add(source)
    return HttpResponseRedirect('/'+str(sessionID))

@login_required
def removesource(request, sessionID, source_name):
    sessionID = int(sessionID)
    sessions = Session.objects.filter(user=request.user)
    session = sessions.get(sessionID=sessionID)
    source = session.sources.get(name=source_name)
    session.sources.remove(source)
    return HttpResponseRedirect('/'+str(sessionID))

    
@login_required
def addmonitor(request, sessionID):
    sessionID = int(sessionID)
    sessions = Session.objects.filter(user=request.user)
    session = sessions.get(sessionID=sessionID)
    if request.method == 'POST':
        form = AddSiteForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            url = form.cleaned_data['url']
            keywords = form.cleaned_data['keywords']
            try:
                site = Site.objects.get(name=name)
                if not(site in session.monitors.all()):
                    session.monitors.add(site)
            except Site.DoesNotExist:
                site = Site(name=name, url=url, keywords=keywords)
                site.save()
                session.monitors.add(site)
            return HttpResponseRedirect('/'+str(sessionID))
        else:
            return render(request, "siteList.html", {'form': form, 'sessions': sessions, 'session' : session, 'sessionID': sessionID, 'source': False})
    else:
        form = AddSiteForm()
        return render(request, "siteList.html", {'form': form, 'sessions': sessions, 'session' : session, 'sessionID': sessionID, 'source': False})

@login_required
def addexistingmonitor(request, sessionID, monitor_name):
    sessionID = int(sessionID)
    sessions = Session.objects.filter(user=request.user)
    session = sessions.get(sessionID=sessionID)
    monitor = Site.objects.get(name=monitor_name)
    session.monitors.add(monitor)
    return HttpResponseRedirect('/'+str(sessionID))

@login_required
def removemonitor(request, sessionID, monitor_name):
    sessionID = int(sessionID)
    sessions = Session.objects.filter(user=request.user)
    session = sessions.get(sessionID=sessionID)
    monitor = session.monitors.get(name=monitor_name)
    session.monitors.remove(monitor)
    return HttpResponseRedirect('/'+str(sessionID))

#def home(request):
#     # Like before, get the request's context.
#    context = RequestContext(request)
#
#    # A boolean value for telling the template whether the registration was successful.
#    # Set to False initially. Code changes value to True when registration succeeds.
#    registered = False
#
#    # If it's a HTTP POST, we're interested in processing form data.
#    if request.method == 'POST':
#        # Attempt to grab information from the raw form information.
#        # Note that we make use of both UserForm and UserProfileForm.
#        user_form = UserForm(data=request.POST)
#
#        # If the two forms are valid...
#        if user_form.is_valid() :
#            # Save the user's form data to the database.
#            user = user_form.save()
#
#            # Now we hash the password with the set_password method.
#            # Once hashed, we can update the user object.
#            user.set_password(user.password)
#            user.save()
#
#            # Now sort out the UserProfile instance.
#            # Since we need to set the user attribute ourselves, we set commit=False.
#            # This delays saving the model until we're ready to avoid integrity problems.
#
#            # Update our variable to tell the template registration was successful.
#            registered = True
#
#        # Invalid form or forms - mistakes or something else?
#        # Print problems to the terminal.
#        # They'll also be shown to the user.
#        else:
#            print user_form.errors
#
#    # Not a HTTP POST, so we render our form using two ModelForm instances.
#    # These forms will be blank, ready for user input.
#    else:
#        user_form = UserForm()
#
#    # Render the template depending on the context.
#    return render_to_response("home.html",
#                              locals(),
#                              context_instance = RequestContext(request)
#                              )
def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() :
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render_to_response(
            'register.html',
            {'user_form': user_form, 'registered': registered},
            context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponseRedirect('/invalidUser/')

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response("login.html",locals(), context_instance = RequestContext(request))

def invalidUser(request):
    return render_to_response("invalidUser.html",locals(), context_instance = RequestContext(request))


@login_required
def crawling(request, sessionID):
    sessions = Session.objects.filter(user=request.user)
    session = sessions.get(sessionID=sessionID)
    crawl_domain.delay(session.id)
    return HttpResponseRedirect('/'+sessionID)

@login_required
def thankspage(request):
    return render_to_response("thankyou.html",locals(), context_instance = RequestContext(request))

def about(request):
    return render_to_response("about.html",locals(), context_instance = RequestContext(request))

@login_required
def results(request, sessionID):
    sessionID = int(sessionID)
    sourceNames =  []
    sessions = Session.objects.filter(user=request.user)
    mysession = sessions.get(sessionID=sessionID)
    sessionMonitors = mysession.monitors.all()
    sessionSources = mysession.sources.all()
    allLog = resultLogData.objects.all()
    for u in allLog:
        if int(u.sessionID) == sessionID:
            resultLogData.delete(u)
    allLog = resultLogData.objects.all()
    p = []
    for i in allLog:
        p.append(int(i.sessionID))
    lengthList = []
    for sources in sessionMonitors:
        lengthList.append(len(crawlData.objects.filter(article_url__startswith = sources.url).filter(in_resultID=mysession.result_count)))
        sourceNames = list(chain(sourceNames,crawlData.objects.filter(article_url__startswith = sources.url).filter(in_resultID=mysession.result_count)))
    return render_to_response("results.html",
                              locals(),
                              context_instance = RequestContext(request)
                              )

@login_required
def summary(request, sessionID):
    sessionID = int(sessionID)
    monitorNames =  []
    sessions = Session.objects.filter(user=request.user)
    mysession = sessions.get(sessionID=sessionID)
    sessionMonitors = mysession.monitors.all()
    lengthList = []
    allLog = resultLogData.objects.all()
    p = []
    for i in allLog:
        p.append(int(i.sessionID))
    for monitors in sessionMonitors:
        lengthList.append(len(crawlData.objects.filter(article_url__startswith = monitors.url).filter(in_resultID=mysession.result_count)))
        monitorNames = list(chain(monitorNames,crawlData.objects.filter(article_url__startswith = monitors.url).filter(in_resultID=mysession.result_count)))
    dict = {}
    return render_to_response("summary.html",
                              locals(),
                              context_instance = RequestContext(request)
                              )

    #k = Person.objects.all()
    #crawleddata = CrawledData.objects.all()
    #visualizationdata = [["Lookingfor", "NYTIMES"]]
    #for data in crawleddata:
    #    visualizationdata.append([data.lookingfor, data.hits])
    #
    #return render_to_response("results.html",
    #                            locals(),
    #                            context_instance = RequestContext(request)
    #                          )
#return(HttpResponseRedirect("http://www.google.com"))
#@login_required
#def job(request):
#    form = JobForm(request.POST or None)
#    k =  WebSites.objects.filter(owner__username = request.user.username)
#    if form.is_valid():
#        add = form.cleaned_data['urlinput']
#        a = WebSites(urlname= add, owner= request.user)
#        i = 0
#        for f in k:
#            if f.urlname == add:
#                i =1
#        if i == 0:        
#            a.save()
#        else:
#            messages.success(request, "already have that url")
#        if not (add in l):
#            l.append(str(add))
#        messages.success(request, str(l))
#    return render_to_response("job.html",
#                              locals(),
#                              context_instance = RequestContext(request)
#                              )
