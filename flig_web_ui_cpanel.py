#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import cgi,os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template


class UI_CPanel(webapp.RequestHandler):
	def get(self):
		#self.response.out.write(GenPhotosetList(USER_ID))


		CUser = users.get_current_user()

		if CUser:
			if users.is_current_user_admin():
				
				#==Обработать Ошибку
				Photosets=self.GetPhotosets()
				
				Template_values = {
					"Photosets": Photosets,
					"Update_url":"/update_gal?photoset_id=",
					"Logout_url":users.create_logout_url(self.request.uri),
					"PhotosetsUpdURL":"/update_gal?photoset_id=1111111111"
					}
				
				path = os.path.join(os.path.dirname(__file__), "templates/ui_cpanel.html")
				self.response.out.write(template.render(path, Template_values))
			else:
				#self.redirect(users.create_logout_url(self.request.uri))
				#self.response.out.write('not admin')
				self.response.out.write("You are not authorized to view this page")
				self.response.out.write(" <a href='"+users.create_login_url(self.request.uri)+"'> Relogin</a>")
		else:
			self.redirect(users.create_login_url(self.request.uri))
			
	def GetPhotosets(self):				
		return db.GqlQuery("SELECT * FROM Photosets").fetch(1000)