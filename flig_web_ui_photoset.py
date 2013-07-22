#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import db		
from jinja2 import Markup, escape

""" Convert linebreaks to <br/>s and escape each line.  Return value is marked 'safe' """
def linebreaksbr(value):
    lines = []
    for line in value.split('\n'):
        lines.append(line)
    result = "<br/>".join(lines)
    return Markup(result)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])
JINJA_ENVIRONMENT.filters['linebreaksbr'] = linebreaksbr

class UIPhotoset(webapp2.RequestHandler):
	def get(self):
		photoset_id = self.request.get('id')
		       
		template_values = {
			"Photos": self.get_photoset_photos(photoset_id),
            "Photoset_title": self.get_photoset_title(photoset_id),
            "RefreshLink":""
			}
			
		current_user = users.get_current_user()
		if current_user:
			if users.is_current_user_admin():
				template_values["RefreshLink"] = "".join(["<a href='/update_gal?photoset_id=",photoset_id,"'> Refresh</a>"])
			else:
				template_values["RefreshLink"] = ""
		else:
			template_values["RefreshLink"] = "".join(["<a  href='",users.create_login_url(self.request.uri),"'> *</a>"])

		template = JINJA_ENVIRONMENT.get_template('templates/ui_photoset.html')
		self.response.write(template.render(template_values))
        
	def get_photoset_photos(self,photoset_id):
		return db.GqlQuery("SELECT * FROM Photos where photoset_id=:1 and isprimary=false ORDER BY order_id",photoset_id).fetch(1000)
    
	def get_photoset_title(self,photoset_id):
		return db.GqlQuery("SELECT * FROM Photosets where photoset_id=:1",photoset_id).get().title