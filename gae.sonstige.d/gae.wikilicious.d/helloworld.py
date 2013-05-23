from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from MainLib import fn_write_ganalytics
        
class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        self.response.out.write("<html><head><title>hello</title>")        
        fn_write_ganalytics(self.response.out)
        self.response.out.write("</head><body>")        
        self.response.out.write('Hello, webapp World!')
        self.response.out.write("</body></html>")        
        
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')

application = webapp.WSGIApplication([('/', MainPage)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
