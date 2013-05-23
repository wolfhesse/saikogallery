from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from exper_reference_model import MyList, MyName
import random

FACEBOOK_APP_ID = None

class BaseHandler(webapp.RequestHandler):
    """Provides access to the active Facebook user in self.current_user

    The property is lazy-loaded on first access, using the cookie saved
    by the Facebook JavaScript SDK to determine the user ID of the active
    user. See http://developers.facebook.com/docs/authentication/ for
    more information.
    """
    @property
    def current_user(self):
        if not hasattr(self, "_current_user"):
            self._current_user = None
        return self._current_user
    
    @property
    def my_list(self):
        if not hasattr(self, "_my_list"):
            self._my_list = None
            mylist = MyList.all()
            if not mylist == None:
                self._my_list = mylist
        return self._my_list

class HomeHandler(BaseHandler):
    
    def action_new(self):
        l = MyList()
        l.name="list %s" % random.randint(0,22000)
        l.put()
        
        for x in (0,2,4,8,6,10):
            n1 = MyName()
            n1.short_desc = "short desc %s %s" % (x,random.randint(0,100))
            n1.listed_in_list = l
            n1.put()
        self.redirect("/exper_reference") # default redirect, if it not happened already    
       
    def action_delall(self):
        ## da brauch ich eine bremse... sagen wir, 50 deletes sind ok
        count=0
        l = MyList.all()
        for x in l:
            for y in x.myname_set:
                y.delete()
            x.delete()
            count+=1
            if count > 50:
                return
            
       
    def get(self):
        redirections = {"new":self.action_new,"delall":self.action_delall}
        action = self.request.get("action")
        if action != '':
            redirections[action]()
            
     
        my_list = self.my_list
          
        path = os.path.join(os.path.dirname(__file__), "exper_reference.html")
        args = dict(current_user=self.current_user,
                    my_list = my_list,
                    facebook_app_id=FACEBOOK_APP_ID)
        self.response.out.write(template.render(path, args))
    
application = webapp.WSGIApplication([('.*', HomeHandler) ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
