from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class FbAugarten(webapp.RequestHandler):

    def __init__(self):
        pass

    def handle_request(self):
        self.response.headers['Content-Type'] = 'text/html'
        #self.response.out.write('<pre>query is %s</pre>' % str(self.request))
        self.response.out.write('<hr />Hello, Augarten!')
        self.response.out.write('<hr /><fb:bookmark type="off-facebook"></fb:bookmark>')

    def post(self):
        self.handle_request()
    def get(self):
        self.handle_request()



application = webapp.WSGIApplication([('.*', FbAugarten) ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
