
import datetime
import cgi
import os
import wsgiref.handlers


from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required


import gdata.service
import gdata.urlfetch
gdata.service.http_request_handler = gdata.urlfetch

import gdata.spreadsheet.text_db
import pickle

class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    
    def cleanstru(self):
        attribs=[]
        for a in ['author','content','date']:
            attribs = attribs + [{a:str(eval("self."+a))}]
        return { 'Greeting':attribs }

class DocFile(db.Model):
    doc_name=db.StringProperty()
    doc_file=db.BlobProperty()
    
class TestA(webapp.RequestHandler):
    @login_required
    def get(self):
        
        client = gdata.spreadsheet.text_db.DatabaseClient()
        client.SetCredentials('ohramweltgeschehen','kidman')
        
        databases=client.GetDatabases(name='geo20080813')
        sdb=databases[0]
        
        tables=sdb.GetTables(name='')
        table=tables[0]
        records=table.GetRecords(1,100)
        
        
        for r in records:
            q = db.GqlQuery("SELECT * FROM DocFile WHERE doc_name = :1", r.content['name'])
            results = q.fetch(1)
            if results:
                doc = results[0]
                doc.doc_file = doc.doc_file + r.content['address']
            else:
                doc = DocFile()
                doc.doc_name = r.content['name']
                doc.doc_file = r.content['address']
            doc.put()
            
        ap=[r.content['pickled'] for r in records]
        au=[pickle.loads(i) for i in ap]
#        try:
#            mail.send_mail(sender="rogeraaut@gmail.com",
#                  to="ohramweltgeschehen@gmail.com",
#                  subject="[gae:mhs]test",
#                  body="""
#Dear Albert:
#
#Your example.com account has been approved.  You can now visit
#http://www.example.com/ and sign in using your Google Account to
#access new features.
#
#Please let us know if you have any questions.
#
#The example.com Team
#""")
#        except:
#            #print 'mail-err 1'
#            pass
        
        try:
            message = mail.EmailMessage()
            message.sender = "rogeraaut@gmail.com"
            message.to = "ohramweltgeschehen@gmail.com"
            message.body = """
    I've invited you to Example.com!

    To accept this invitation, click the following link,
    or copy and paste the URL into your browser's address
    bar:

    %s
    """ % "rogera"

            message.send()
        except:
            #print 'mail-err 2'
            pass    

#        au = { 'no socket' : 'so, no database access' }
        template_values = {'au':au}
        
        path = os.path.join(os.path.dirname(__file__), 'testA.html')
        self.response.out.write(template.render(path, template_values))
        
class TestB(webapp.RequestHandler):
    def get(self):
        qg=Greeting.all().order('-date')
        cg=qg.fetch(100)
        template_values = { 'cg': cg }
        
        path = os.path.join(os.path.dirname(__file__), 'testB.html')
        self.response.out.write(template.render(path, template_values))
        
class YpData(webapp.RequestHandler):
    def get(self):
        template_values = {}
        
        path = os.path.join(os.path.dirname(__file__), 'ypdata.html')
        self.response.out.write(template.render(path, template_values))
        
        
class MainPage(webapp.RequestHandler):
    def get(self):
    
        dtme=datetime.datetime(1,1,1).now().time()

        template_values = {
                'dtme': str(dtme),
                }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
        
def main():
    application = webapp.WSGIApplication(
        [('/', MainPage),
         ('/ypdata',YpData),
         ('/testA', TestA),
         ('/testB', TestB),
         ],
        debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()

