from google.appengine.ext import webapp
from google.appengine.ext.webapp import template, util
from google.appengine.ext.webapp.util import run_wsgi_app
from wl_user_model import WlUser
import facebook


FACEBOOK_APP_ID = "290014515429"
FACEBOOK_APP_SECRET = "527e99b2f756b061d5c176234668df67"


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


class FbAugarten(BaseHandler):

    def __init__(self):
        pass

    def handle_request(self):
        self.response.headers['Content-Type'] = 'text/html'
        #self.response.out.write('<pre>query is %s</pre>' % str(self.request))
        self.response.out.write('<hr />Hello, Augarten!')
        #self.response.out.write('<hr /><fb:bookmark type="off-facebook"></fb:bookmark>')
#        path = os.path.join(os.path.dirname(__file__), "fb_anfrage2.html")
#        cstr = 'init;'
#        for c in self.request.cookies:
#            cstr = cstr + 'c:' + c + ', cc:' + self.request.cookies[c]
#        cstr += '||len = ' + str(len(self.request.cookies))
#        args = dict(current_user=self.current_user,
#                    facebook_app_id=FACEBOOK_APP_ID,
#                    cookies=cstr)
#        self.response.out.write(template.render(path, args))
        self.response.out.write('<hr /><fb:iframe src="http://84.113.229.194/fb_anfrage/" frameborder=0 smartsize=true />')
        
    def post(self):
        self.handle_request()
    def get(self):
        self.handle_request()



application = webapp.WSGIApplication([('.*', FbAugarten) ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
