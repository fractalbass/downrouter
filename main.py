#  Downrouter.  Created by Miles Porter.  August 15, 2012
#
import webapp2
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import os
from google.appengine.ext.webapp import template
import logging
from datetime import datetime

from data_model import MobileRedirect, API_KEY

class BaseHandler(webapp.RequestHandler):
    def render_template(self, template_name, template_values):
        path = os.path.join(os.path.dirname(__file__), template_name)
        self.response.out.write(template.render(path, template_values))

class MainHandler(BaseHandler):
    def get(self):
        api_key_str = self.request.get('api_key')
        api = API_KEY.all().filter('api_key =', api_key_str)
        if api.count()==0:
            self.render_template("invalid.html", {})
        elif api[0].expires < datetime.now():
            self.render_template("expired.html", {})
        else:
            user_agent = self.request.get('UA', None)
            if not user_agent:
                user_agent = str(self.request.headers['User-Agent'])
            logging.info("User agent is: %s" % user_agent)

            redirect = "None"
            for p in self.request.arguments():
                if p.upper() in user_agent.upper():
                    redirect = self.request.get(p)

                    m = MobileRedirect(parameter_string=self.request.query_string,
                        user_agent = user_agent,
                        resulting_url = redirect)
                    m.put()

            if redirect=="None":
                redirect = self.request.get('DEFAULT', "NoDefault")

            if redirect == "NoDefault":
                render_template("info.html", {})
                #path = os.path.join(os.path.dirname(__file__), 'info.html')
                #self.response.out.write(template.render(path, {}))
            else:
                logging.info("Redirecting to %s" % redirect)
                self.redirect(str(redirect))

app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)
