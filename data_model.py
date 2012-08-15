from google.appengine.ext import db

__author__ = 'miles_r_porter'

class MobileRedirect(db.Model):
    user_agent = db.StringProperty(required=True)
    parameter_string = db.StringProperty()
    resulting_url = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class API_KEY(db.Model):
    api_key = db.StringProperty(required=True)
    account_name = db.StringProperty(required=True)
    expires = db.DateTimeProperty(required=True)
    email = db.StringProperty(required=True)
    description = db.StringProperty(required=True)
    account_number = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now=True)
