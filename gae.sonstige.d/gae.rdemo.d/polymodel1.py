from google.appengine.ext.db import polymodel
from google.appengine.ext import db


class Contact(polymodel.PolyModel):
    phone_number = db.PhoneNumberProperty()
    address = db.PostalAddressProperty()
    flg_deleted = db.BooleanProperty(False)

class Person(Contact):

    def get_first_name(self):
        return self.first_name

    first_name = db.StringProperty()
    last_name = db.StringProperty()
    mobile_number = db.PhoneNumberProperty()
        
    @property
    def name(self):
        #return '{0}, {1}'.format(self.last_name, self.p_first_name)
        return "%s, %s" % (self.last_name, self.first_name)
    p_first_name = property(get_first_name, None, None, None)
    
class Company(Contact):
    name = db.StringProperty()
    fax_number = db.PhoneNumberProperty()