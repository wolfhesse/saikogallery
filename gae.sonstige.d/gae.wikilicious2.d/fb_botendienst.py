import webapp2

from MainLib import fn_write_ganalytics, fn_write_fbjs

class FbBotendienstHandler(webapp2.RequestHandler):


    def handle_request(self):
        self._red = None
        self._bas = None
      
        i = self.request.path.find('bd')
        if i > 0:
            self._red = self.request.path[i:] 
            self._bas = self.request.path[:i]
            #self.response.redirect('http://apps.facebook.com/botendienst/21?red=21')

        self.response.headers['Content-Type'] = 'text/html'
        
        #self.response.out.write("der hallo %s" % self._red)
        #self.response.out.write('<pre>path is %s</pre>' % self.request.path)
        
        if self._red != None:
            self.response.out.write("<title>Guter Botendienst %s </title>" % self._red)
            self.response.out.write('<hr /><fb:name uid="853022289" ></fb:name>')
            self.response.out.write('<p><a href="%s">Verzeichnis</a></>' % self._bas)
            self.response.out.write('<hr /><h2>Beispielbotendienst %s</h2>' % self._red)
            self.response.out.write("<br /><fb:comments xid='fb_botendienst_beispiel_%s'></fb:comments>" % self._red)
        else:    
            self.response.out.write('<hr /><h2>Beispielbotendienste:</h2>')
            self.response.out.write('<ul>')
            self.response.out.write('<li><a href="./bd22">botendienst 22</a></li>')
            self.response.out.write('<li><a href="./bd23">botendienst 23</a></li>')
            self.response.out.write('<li><a href="./bd24">botendienst 24</a></li>')
            self.response.out.write('<li><a href="./bd25">botendienst 25</a></li>')
            self.response.out.write('</ul>')
                           
            self.response.out.write('<br /><fb:comments xid="fb_botendienst_beispiel"></fb:comments>')
            
            self.response.out.write("<h2>und was anderes...</h2>")
            self.response.out.write('<ul>')
            self.response.out.write('<li><a href="/static/sample-1.html">Sample 1</a></li>')
            self.response.out.write('<li><a href="/static/sample-2.html">Sample 2</a></li>')
            self.response.out.write('<li><a href="/static/sample-3.html">Sample 3</a></li>')
            self.response.out.write('<li><a href="/static/sample-4.html">Sample 4</a></li>')
            self.response.out.write('<li><a href="/static/wikilicious.html">wikilicious</a></li>')
            self.response.out.write('</ul>')
             
        fn_write_ganalytics(self.response.out)
        fn_write_fbjs(self.response.out)

    def post(self):
        self.handle_request()
    def get(self):
        # debug - zweig
        self.handle_request()
        #usercoll = WlUser.all()
        #for user in usercoll:
        #    print repr(user.name)

app = webapp2.WSGIApplication([('.*', FbBotendienstHandler) ], debug=True)

