#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import flig_db
import cgi
import datetime
import webapp2
from google.appengine.api import users


class WRK_UpdateGal(webapp2.RequestHandler):
	def get(self):
		USER_ID="46978340@N08"
		
		CUser = users.get_current_user()
		if CUser:
			if users.is_current_user_admin():
				Photosets = []
				PhotosetID=cgi.escape(self.request.get('photoset_id'))
				
				if PhotosetID:
					if PhotosetID=='1111111111':
						UpdateResult=flig_db.UpdatePhotosets(USER_ID)
						if UpdateResult=="ok":
							self.redirect("/")
						else:
							self.response.write('Update Photosets list: ')
							self.response.write(UpdateResult)
					else:
						UpdateResult=flig_db.UpdatePhotos(PhotosetID)
						if UpdateResult=="ok":
							self.redirect("/photoset?id="+PhotosetID)
						else:
							self.response.write('Update photoset '+PhotosetID+': ')
							self.response.write(UpdateResult)

			else:
				self.redirect(users.create_login_url(self.request.uri))

		else:
			self.redirect(users.create_login_url(self.request.uri))