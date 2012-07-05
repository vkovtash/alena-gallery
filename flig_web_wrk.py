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

import flig_db

import cgi
import datetime
from google.appengine.api import users
from google.appengine.ext import webapp


class WRK_UpdateGal(webapp.RequestHandler):
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
							self.response.out.write('Update Photosets list: ')
							self.response.out.write(UpdateResult)
					else:
						UpdateResult=flig_db.UpdatePhotos(PhotosetID)
						if UpdateResult=="ok":
							self.redirect("/photoset?id="+PhotosetID)
						else:
							self.response.out.write('Update photoset '+PhotosetID+': ')
							self.response.out.write(UpdateResult)

			else:
				self.redirect(users.create_login_url(self.request.uri))

		else:
			self.redirect(users.create_login_url(self.request.uri))