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


from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import users
from datetime import datetime
import cgi

class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class MainHandler(webapp.RequestHandler):
    def fn_create_greeting_now(self, greeting):
        if users.get_current_user():
            greeting.author = users.get_current_user()
        self.d = datetime.now()
        greeting.content = str('Hello world! @ %s' % str(self.d))
        greeting.put()

    def fn_print_all_greetings(self):
        greetings = db.GqlQuery("SELECT * "
        "FROM Greeting "
        "ORDER BY date DESC LIMIT 10")

        for greeting in greetings:
            if greeting.author:
                self.response.out.write('<b>%s</b> wrote:' % greeting.author.nickname())
            else:
                self.response.out.write('An anonymous person wrote:')
                self.response.out.write('<blockquote>%s</blockquote>' % cgi.escape(greeting.content))

    def get(self):
        self.response.out.write('<title>gae:localltop</title>')
        self.fn_print_all_greetings()
        greeting = Greeting()
        self.fn_create_greeting_now(greeting)
        self.response.out.write(greeting.content)

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
