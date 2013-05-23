#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util
from wl_user_model import WlUser
from google.appengine.ext.db import polymodel
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from polymodel1 import Person, Contact, Company

class PersonHandler(webapp.RequestHandler):
    
    def post(self,id,rest=None):
        self.response.out.write(self.request.params)
        #name = self.request.params.get('name')
        u = WlUser.get_by_key_name(id)
        if u != None:
            nm = self.request.get('name')
            if u != '':
                u.name = nm 
            at = self.request.get('access_token')
            if at != '':
                u.access_token = at
            cm = self.request.get('comment')
            if cm != '':
                u.comment = cm
            u.put()
            self.redirect('/Person/%s?action=show&message=person saved' % id)
        else:
            self.response.out.write("could not find person")
    
    def get(self, id=None, rest=None):
        message = self.request.get('message')
        
        u=None
        if id != '':    
            u = WlUser.get_by_key_name(id)
        if u != None:
            action = self.request.get('action')
            
            if (action=='') or (action == 'show'):
                ## template
                if users.get_current_user():
                    url = users.create_logout_url(self.request.uri)
                    url_linktext = 'Logout'
                else:
                    url = users.create_login_url(self.request.uri)
                    url_linktext = 'Login'
                template_values = {
                    'person':u,
                    'url':url,
                    'message':message,
                    'url_linktext':url_linktext}
                path = os.path.join(os.path.dirname(__file__), 'partial', 'person.html')
                self.response.out.write(template.render(path, template_values))
            else:
                if action == 'edit':
                    self.response.out.write("edit Person")
                else:
                    self.response.out.write("no Person logic for action %s" % action)
                
class WlUserHandler(webapp.RequestHandler):

    def render_partial_person(self):
        k = self.request.get('name')
        u = WlUser.get_by_key_name(k)
        if u != None:
        ## template
            if users.get_current_user():
                url = users.create_logout_url(self.request.uri)
                url_linktext = 'Logout'
            else:
                url = users.create_login_url(self.request.uri)
                url_linktext = 'Login'
            template_values = {
                'person':u,
                'url':url,
                'url_linktext':url_linktext}
            path = os.path.join(os.path.dirname(__file__), 'partial', 'person.html')
            self.response.out.write(template.render(path, template_values))
        return

    def get(self):
        path = self.request.path
        sub = str.replace(path, '/WlUser/', '')
        sub2 = path.replace('/WlUser/', '')
        args = self.request.arguments()
        
        self.response.headers['Content-Type'] = 'text/html'
        
        if(sub2.find('Person') > -1):
            self.render_partial_person()
        
        
        self.response.out.write("<pre>")
        self.response.out.write("<br />sub was: %s" % sub)
        self.response.out.write("<br />sub2 was: %s" % sub2)
        self.response.out.write("<br />path was: %s" % path)
        self.response.out.write("<br />args was: %s" % args)
        
class MainHandler(webapp.RequestHandler):
    def get(self):
        
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write("<title>rdemo</title>")
        self.response.out.write("<pre>")        
        p = Person(phone_number='1-206-555-9234',
                   address='123 First Ave., Seattle, WA, 98101',
                   first_name='Alfred',
                   last_name='Smith',
                   mobile_number='1-206-555-0117')
        p.put()
        
        c = Company(phone_number='1-503-555-9123',
                    address='P.O. Box 98765, Salem, OR, 97301',
                    name='Data Solutions, LLC',
                    fax_number='1-503-555-6622', flg_deleted=False)
        c.put()
        
        for contact in Contact.all():
            # Returns both p and c.
            # ...
            if not contact.flg_deleted: self.response.out.write("Contact: %s; %s \n" % (contact.address, contact.name))
            else: self.response.out.write("...deleted Contact...\n")
        
        for person in Person.all():
            # Returns only p.
            # ...
            if not person.flg_deleted: self.response.out.write("Person: %s; %s\n" % (person.address, person.name))     

             
        for x in Contact.all(): x.flg_deleted = True;x.put()
                    
        #for u in WlUser.all():
        #    u.delete()
        uc = WlUser.all()
        #print uc.count()
        if uc.count() < 1:
            u = WlUser(key_name='roger', id='roger', profile_url='http://', access_token='a', name="Roger")
            u.put()
        r = WlUser.get_by_key_name("roger")
        self.response.out.write("<a href='http://google.com'>google</a><br />")
        self.response.out.write('Hello world! %s ' % r.name)


def main():
    application = webapp.WSGIApplication([
                                          ('/WlUser/.*', WlUserHandler),
                                          ('/Person/(.*)', PersonHandler),
                                          ('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
