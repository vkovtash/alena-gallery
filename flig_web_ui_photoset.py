#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import webapp2
import jinja2
import cgi
import os
from google.appengine.api import users
from google.appengine.ext import db		
from jinja2 import Markup, escape

""" Convert linebreaks to <br/>s and escape each line.  Return value is marked 'safe' """
def linebreaksbr(value):
    escaped_lines = []
    for line in value.split('\n'):
        escaped_lines.append(escape(line))
    escaped = "<br/>".join(escaped_lines)
    # mark as safe
    return Markup(escaped)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])
JINJA_ENVIRONMENT.filters['linebreaksbr'] = linebreaksbr

class UI_Photoset(webapp2.RequestHandler):
	def get(self):
		PhotosetID=cgi.escape(self.request.get('id'))
		       
		Tmain_values = {
			"Photos": self.GetPhotosetPhotos(PhotosetID),
            "Photoset_title": self.GetPhotosetTitle(PhotosetID),
            "RefreshLink":""
			}
			
		CUser = users.get_current_user()
		if CUser:
			if users.is_current_user_admin():
				Tmain_values["RefreshLink"]="<a href='/update_gal?photoset_id="+PhotosetID+"'> Refresh</a>"
			else:
				Tmain_values["RefreshLink"]=""
		else:
			Tmain_values["RefreshLink"]="<a  href='"+users.create_login_url(self.request.uri)+"'> *</a>"

		template = JINJA_ENVIRONMENT.get_template('templates/ui_photoset.html')
		self.response.write(template.render(Tmain_values))
        
	def GetPhotosetPhotos(self,PhotosetID):
		return db.GqlQuery("SELECT * FROM Photos where photoset_id=:1 and isprimary=false ORDER BY order_id",PhotosetID).fetch(1000)
    
	def GetPhotosetTitle(self,PhotosetID):
		return db.GqlQuery("SELECT * FROM Photosets where photoset_id=:1",PhotosetID).get().title