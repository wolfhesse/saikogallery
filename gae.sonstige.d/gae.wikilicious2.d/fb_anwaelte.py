
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template, util
from google.appengine.ext.webapp.util import run_wsgi_app
from wl_user_model import WlUser
import facebook
import os.path
import wsgiref.handlers




FACEBOOK_APP_ID = "51957578229"
FACEBOOK_APP_SECRET = "d511da595001440dedf993ed89a9f113"


class BaseHandler(webapp.RequestHandler):
    """Provides access to the active Facebook user in self.current_user

    The property is lazy-loaded on first access, using the cookie saved
    by the Facebook JavaScript SDK to determine the user ID of the active
    user. See http://developers.facebook.com/docs/authentication/ for
    more information.
    """
    @property
    def current_part(self):
        if not hasattr(self, "_current_part"):
            self._current_part = None
            self._current_part='<b>current_part</b>'
        return self._current_part

class HomeHandler(BaseHandler):
    
    def get(self):
        path = os.path.join(os.path.dirname(__file__), "fb_anwaelte.html")
        args = dict(current_part=self.current_part)
        self.response.out.write(template.render(path, args))
    
    def post(self):
        path = os.path.join(os.path.dirname(__file__), "fb_anwaelte.html")
        args = dict(current_part=self.current_part)
        self.response.out.write(template.render(path, args))

application = webapp.WSGIApplication([('.*', HomeHandler) ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
