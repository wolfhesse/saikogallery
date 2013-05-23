import datetime
import cgi
import os
import urllib
import wsgiref.handlers
from django.utils import simplejson
from xml.sax.saxutils import unescape
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from xmlrpclib import ServerProxy, Error
from DekiExt import *
from xmlrpc import *

class Greeting(db.Model):
    obj_key = db.StringProperty(name='key')
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

    def cleanstru(self):
        attribs = {}
        attribs['id'] = str(self.key().id())
        for a in ['author', 'content', 'date']:
            attribs[a] = str(eval("self." + a))
        return { 'Greeting':attribs }

class Erbse(db.Model):
    who = db.UserProperty()
    count = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)

# werbung

class AseController(webapp.RequestHandler):
    def get(self):
        # suche 'rogeraaut' und gib das mit aus
        # query = urllib.urlencode({'q' : 'rogeraaut'})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?q=zahnarzt+wien+1180&v=1.0'
        search_results = urllib.urlopen(url)
        print 'SR: ' + repr(search_results)
        json = simplejson.loads(search_results.read())
        print "JS: " + repr(json)
        results = json['responseData']['results']
        template_values = { 'results' : results, }
        
        path = os.path.join(os.path.dirname(__file__), 'views/ase.html')
        self.response.out.write(template.render(path, template_values))

#  yahoo pipe steiert daten ein
class EchoController(webapp.RequestHandler):
    def get(self):
        self.myresult()

    def post(self):
        greeting = Greeting()

        d = simplejson.loads(self.request.get('data'))
        d3 = d["items"][0]["content"]
        greeting.content = unescape(d3[0:499])
        #greeting.content=unescape(self.request.body[0:400])
        greeting.put()
        self.myresult()

# ausgabe eines rss streams

    def myresult(self):
        greetings_query = Greeting.all().order('-date')
        greetings = greetings_query.fetch(10)

        d = datetime.datetime(1, 1, 1).now()

        response = str(d)
        template_values = {
                'd':d,
                'greetings':greetings,
                }
        path = os.path.join(os.path.dirname(__file__), 'views/echo.xml')
        self.response.out.write(template.render(path, template_values))

# das erbsenzaehlenspiel mit gespeichertem 'highscore'
class ErbsenzaehlenController(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        erbsen_who = None
        erbsen_all = None
        if user:
            erbsen_all_query = Erbse.all().order('-count')
            erbsen_all = erbsen_all_query.fetch(10)

            erbsen_who_query = Erbse.gql('WHERE who = :1', user)
            erbsen_who = erbsen_who_query.get()

            if erbsen_who == None:
                erbsen_who = Erbse()
                erbsen_who.who = users.get_current_user()
                erbsen_who.count = 0
                erbsen_who.put()
        else:
            self.redirect(users.create_login_url(self.request.uri))

        template_values = {
                'erbsen_who': erbsen_who,
                'erbsen_all': erbsen_all,
                }

        path = os.path.join(os.path.dirname(__file__), 'views/ez.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        user = users.get_current_user()
        erbsen_who_query = Erbse.gql('WHERE who = :1', user)
        erbsen_who = erbsen_who_query.get()
        erbsen_who.who = user
        erbsen_who.count = int(self.request.get('count'))
        erbsen_who.put()

# xmlrpc handler
class Extimpl:
    def cutfive(self):
        qg = Greeting.all().order('-date')
        # delete if more than 5 entries
        # might need more calls to dense out
        i = 0
        for g in qg.fetch(100):
            i = i + 1
            if i > 5:
                g.delete()

    def greetings(self):
        qg = Greeting.all().order('-date')
        cg = [g.cleanstru() for g in qg.fetch(5)]

        return  simplejson.dumps(cg)

    def add_greeting(self, content):
        g = Greeting()
        g.content = content
        if users.get_current_user():
            greeting.author = users.get_current_user()
        g.put()
        return "OK: " + content

# xmlrpc aufruf aus gae
class FruehlingsrolleController(webapp.RequestHandler):
    def get(self):
        g = Greeting()
        g.content = 'fr xmlrpc call'
        g.put()

        #s=ServerProxy('http://localhost:9020/RPC2', GAEXMLRPCTransport())
        s = ServerProxy('http://blog.fruehlingsrolle.cn/RPC2', GAEXMLRPCTransport())
        gtext = s.greetings()
        template_values = { 'gtext': gtext, }

        path = os.path.join(os.path.dirname(__file__), 'views/fruehlingsrolle.html')
        self.response.out.write(template.render(path, template_values))

# mainpage funktion, json-lieferant
class GuestbookController(webapp.RequestHandler):
    def get(self):
        cbfunc = self.request.get('callback')
        qg = Greeting.all().order('-date')
        cg = [g.cleanstru() for g in qg.fetch(5)]
        r = {'results' : { 'data' : cg }}
        json = simplejson.dumps(r)
        if(str(cbfunc) != ""):
            json = cbfunc + "(" + json + ")"
        self.response.out.write(json)
    def post(self):
        greeting = Greeting()

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')

# xmlrpc server deklaration
class MyExtension(DekiExt):
    def title(self): return "My Extension"
    def description(self): return "My Description"
    def namespace(self): return "my"
    def copyright(self): return "gae:ase:2008:vienna:at"
    def label(self): return "MyExt"

    @function("str", "return user greetings")
    def greetings(self):
        return Extimpl().greetings()

    @function("str", "add greeting")
    @param("str", "text of greeting", True)
    def add_greeting(self, content):
        return Extimpl().add_greeting(content)

# main
class MainPageController(webapp.RequestHandler):
    def get(self):
        dd = datetime.datetime(1, 1, 1).today()
        d = datetime.datetime(1, 1, 1).now()
        dtme = datetime.datetime(1, 1, 1).now().time()

        weekday = dd.weekday()
        wd = ['mo', 'di', 'mi', 'do', 'fr', 'sa', 'so']

        greetings_query = Greeting.all().order('-date')
        greetings = greetings_query.fetch(10)
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'


        template_values = {
                'greetings': greetings,
                'url': url,
                'url_linktext': url_linktext,
                'd': str(d),
                'dd': str(dd),
                'dtme': str(dtme),
                }

        path = os.path.join(os.path.dirname(__file__), 'views/index.html')
        self.response.out.write(template.render(path, template_values))

# werbung mit xmlrpc call auf 'sich selbst'
class SeidenschalController(webapp.RequestHandler):
    def get(self):
        s = ServerProxy('http://r20080614.appspot.com/deki', GAEXMLRPCTransport())
        gtext = s.greetings()
        #gtext = 'not supported'
        template_values = { 'gtext': gtext, }

        path = os.path.join(os.path.dirname(__file__), 'views/seidenschal.html')
        self.response.out.write(template.render(path, template_values))

def main():
    application = webapp.WSGIApplication(
            [('/', MainPageController),
                ('/deki', MyExtension),
                ('/RPC2', MyExtension),
                ('/ase', AseController),
                ('/echo', EchoController),
                ('/ez', ErbsenzaehlenController),
                ('/fruehlingsrolle', FruehlingsrolleController),
                ('/guestbook', GuestbookController), # get
                ('/sign', GuestbookController), # post
                ('/seidenschal', SeidenschalController),
                ],
            debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()

