
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from wl_user_model import WlUser
import facebook
import os.path
import cgi

FACEBOOK_APP_ID = "123054875098"
FACEBOOK_APP_SECRET = "e51d15c1acabde6e15c5675998052d1b"

# Find a JSON parser
try:
    import json
    _parse_json = lambda s: json.loads(s)
except ImportError:
    try:
        import simplejson
        _parse_json = lambda s: simplejson.loads(s)
    except ImportError:
        # For Google AppEngine
        from django.utils import simplejson
        _parse_json = lambda s: simplejson.loads(s)

class BaseHandler(webapp.RequestHandler):
    @property
    def current_cookie(self):
        if not hasattr(self, "_current_cookie"):
            self._current_cookie = None
            cookie = self.request.cookies.get("fbs_" + FACEBOOK_APP_ID, "")
            if not cookie: return None
            args = dict((k, v[-1]) for k, v in cgi.parse_qs(cookie.strip('"')).items())
            if cookie:
                self._current_cookie = cookie
        return self._current_cookie
    
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
            cookie = facebook.get_user_from_cookie(
                self.request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
            if cookie:
                # Store a local instance of the user data so we don't need
                # a round-trip to Facebook on every request
                user = WlUser.get_by_key_name(cookie["uid"])
                if not user:
                    graph = facebook.GraphAPI(cookie["access_token"])
                    profile = graph.get_object("me")
                    user = WlUser(key_name=str(profile["id"]),
                                id=str(profile["id"]),
                                name=profile["name"],
                                profile_url=profile["link"],
                                access_token=cookie["access_token"])
                    user.put()
                elif user.access_token != cookie["access_token"]:
                    user.access_token = cookie["access_token"]
                    user.put()
                self._current_user = user
                
                
        return self._current_user

    @property
    def current_likes(self):
        if not hasattr(self, "_current_likes"):
            self._current_likes = None
            try:
                cookie = facebook.get_user_from_cookie(
                    self.request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
                graph = facebook.GraphAPI(cookie["access_token"])
                uid = cookie["uid"]
                likes = graph.get_connections(uid, "likes")
                self._current_likes = likes["data"]
            except:
                pass
        return self._current_likes

    @property
    def current_links(self):
        if not hasattr(self, "_current_links"):
            self._current_links = None
            try:
                cookie = facebook.get_user_from_cookie(
                    self.request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
                graph = facebook.GraphAPI(cookie["access_token"])
                uid = cookie["uid"]
                links = graph.get_connections(uid, "links", args=[{"limit":25}])
                self._current_links = links["data"]
            except(Exception):
                print 'some error: ' 
                pass
        return self._current_links
    
class HomeHandler(BaseHandler):
    
    def handle_request(self):
        path = os.path.join(os.path.dirname(__file__), "wolfhesse_fbconnect.html")
        args = dict(current_user=self.current_user,
            #current_likes = self.current_likes,
            current_cookie = self.current_cookie,
            current_links = self.current_links,
            current_likes = None,
            fn_parse_json=_parse_json,
            facebook_app_id=FACEBOOK_APP_ID)
        self.response.out.write(template.render(path, args))
    
    def get(self):
        self.handle_request()
    def post(self):
        self.handle_request()
   
application = webapp.WSGIApplication([('.*', HomeHandler) ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
