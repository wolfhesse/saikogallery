from google.appengine.ext import db


class MyList(db.Model):
    name = db.StringProperty()

class MyName(db.Model):
    short_desc= db.StringProperty()
    listed_in_list = db.ReferenceProperty(MyList)
    