from xmlrpclib import ServerProxy, Error
import datetime
s=ServerProxy('http://localhost:8080/deki')
s=ServerProxy('http://r20080614.appspot.com/deki')
s.add_greeting('sample here @ '+str(datetime.datetime.now()))
print s.greetings()