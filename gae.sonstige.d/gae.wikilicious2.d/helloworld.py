# -*- coding: iso-8859-1 -*-
import webapp2

from MainLib import fn_write_ganalytics
        
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        self.response.write("<html><head><title>hello</title>")        
        fn_write_ganalytics(self.response.out)
        self.response.write("""
            <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
        """)
        self.response.write("</head><body>")     
           
        self.response.write('Hello, webapp World!')
        self.response.write('<br />')
        self.response.write('<a href="/static/wikilicious.html">wikilicious</a><br />')
        
        #'''
        self.response.write("""
<hr /><pre>

image copyrights
	
	http://en.wikipedia.org/wiki/File:Moire_Circles.svg
	“File:Moire Circles.svg.” Wikipedia, the Free Encyclopedia. Accessed November 25, 2012. http://en.wikipedia.org/wiki/File:Moire_Circles.svg.
	
</pre>
        """)
        #'''
        self.response.write("""
            <script src="http://code.jquery.com/jquery-latest.js"></script>
            <script src="js/bootstrap.min.js"></script>
        """)
        self.response.write("</body></html>")        
        
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, webapp World!')

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
