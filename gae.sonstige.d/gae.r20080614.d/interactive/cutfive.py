from xmlrpclib import ServerProxy, Error
import datetime

s=ServerProxy('http://r20080614.appspot.com/deki')

#print s.add_greeting('deki sample here @ '+str(datetime.datetime.now()))
#print s.greetings()
print s.cutfive()
 