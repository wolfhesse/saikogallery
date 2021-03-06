
import webapp2
import jinja2

from wl_user_model import WlUser
import facebook
import os.path

FACEBOOK_APP_ID = "51957578229"
FACEBOOK_APP_SECRET = "d511da595001440dedf993ed89a9f113"



 
class BaseHandler(webapp2.RequestHandler):
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

class HomeHandler(BaseHandler):
    
    def get(self):
        jinja_environment = jinja2.Environment(autoescape=True,
           loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
      
        path = "fb_anfrage.html"
        args = dict(current_user=self.current_user,
                    facebook_app_id=FACEBOOK_APP_ID,
                    cookies='get;')
        self.response.write(jinja_environment.get_template(path).render(args))
            
    def post(self):
        jinja_environment = jinja2.Environment(autoescape=True,
           loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
        path =  "fb_anfrage.html"
        cstr='init'
        for c in self.request.cookies:
            cstr = cstr + 'c:' + c + ', cc:' + self.request.cookies[c]
        cstr += '||len = ' + str(len(self.request.cookies))
        args = dict(current_user=self.current_user,
                    facebook_app_id=FACEBOOK_APP_ID,
                    cookies=cstr)
        self.response.write(jinja_environment.get_template(path).render(args))

app = webapp2.WSGIApplication([('.*', HomeHandler) ], debug=True)
    

