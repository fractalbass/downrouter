#  Downrouter.  Created by Miles Porter.  August 15, 2012
#
import webapp2
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import util
import os
from google.appengine.ext.webapp import template
from data_model import API_KEY
from datetime import datetime
from keygen import gen_medium_key, gen_short_key
from google.appengine.ext.webapp.util import login_required

from data_model import MobileRedirect

class AdminHandler(webapp.RequestHandler):

    @login_required
    def get(self):
        user = users.get_current_user()
        logout_url = users.create_logout_url("/")
        api_keys = API_KEY.all()
        path = os.path.join(os.path.dirname(__file__), 'admin.html')
        self.response.out.write(template.render(path, {'api_keys':api_keys, 'user':user, 'logout_url':logout_url}))

    @login_required
    def post(self):
        user = users.get_current_user()
        logout_url = users.create_logout_url("/")
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
        self.response.out.write(template.render(path, {'api_keys':api_keys, 'message':"API Key Created.", 'user':user, 'logout_url':logout_url}))


app = webapp2.WSGIApplication([('/admin/main', AdminHandler)],
    debug=True)