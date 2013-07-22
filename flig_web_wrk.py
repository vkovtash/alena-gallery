#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import flig_db
import webapp2
from google.appengine.api import users

USER_ID="46978340@N08"

class WRKUpdateGal(webapp2.RequestHandler):
	def get(self):
		current_user = users.get_current_user()
		if current_user:
			if users.is_current_user_admin():
				photoset_id = self.request.get('photoset_id',default_value=None)

				if photoset_id is None:
					update_result = flig_db.UpdatePhotosets(USER_ID)
					if update_result == "ok":
						self.redirect("/")
					else:
						self.response.write('Update Photosets list: %s'%update_result)
				else:
					update_result = flig_db.UpdatePhotos(photoset_id)
					if update_result == "ok":
						self.redirect("/photoset?id=%s"%photoset_id)
					else:
						self.response.write('Update photoset %s: %s'%(photoset_id, update_result))
			else:
				self.redirect(users.create_login_url(self.request.uri))
		else:
			self.redirect(users.create_login_url(self.request.uri))