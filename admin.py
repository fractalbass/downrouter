#  Downrouter.  Created by Miles Porter.  August 15, 2012
#
import webapp2
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import os
from google.appengine.ext.webapp import template
from data_model import API_KEY
from datetime import datetime
from keygen import gen_medium_key, gen_short_key

from data_model import MobileRedirect

class AdminHandler(webapp.RequestHandler):

    def get(self):
        api_keys = API_KEY.all()
        path = os.path.join(os.path.dirname(__file__), 'admin.html')
        self.response.out.write(template.render(path, {'api_keys':api_keys}))

    def post(self):
        api_key = gen_short_key()
        account_name = self.request.get("account_name")
        description = self.request.get("description")
        expires = datetime.strptime(self.request.get("expires"),"%Y-%m-%d")
        account_number = self.request.get("account_number")
        email = self.request.get("email")
        key = API_KEY(api_key=api_key, account_name=account_name, description=description, expires=expires, account_number=account_number,email=email)
        key.save()
        api_keys = API_KEY.all()
        path = os.path.join(os.path.dirname(__file__), 'admin.html')
        self.response.out.write(template.render(path, {'api_keys':api_keys, 'message':"API Key Created."}))


app = webapp2.WSGIApplication([('/admin/main', AdminHandler)],
    debug=True)