'''
Created on Aug 15, 2010

@author: rogera
'''

def fn_write_ganalytics(stream):
    return stream.write("""<script type = "text/javascript" > 
  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-1997188-6']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga=document.createElement('script'); ga.type='text/javascript'; ga.async=true;
    ga.src=('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s=document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();
</script>""")
    
def fn_write_fbjs(stream):
    return stream.write("""<div id="fb-root"></div>
<script>
  window.fbAsyncInit = function() {
    FB.init({appId: '67980057068', status: true, cookie: true,
             xfbml: true});
  };
  (function() {
    var e = document.createElement('script'); e.async = true;
    e.src = document.location.protocol +
      '//connect.facebook.net/en_US/all.js';
    document.getElementById('fb-root').appendChild(e);
  }());
</script>""")
    