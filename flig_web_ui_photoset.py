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
			

class UI_Photoset(webapp.RequestHandler):
	def get(self):
		
		#==Обработать ошибку
		PhotosetID=cgi.escape(self.request.get('id'))
		
		
		#==Обработать ошибку        
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
				
        
		path = os.path.join(os.path.dirname(__file__), 'templates/ui_photoset.html')
		self.response.out.write(template.render(path, Tmain_values))
        
	def GetPhotosetPhotos(self,PhotosetID):
		return db.GqlQuery("SELECT * FROM Photos where photoset_id=:1 and isprimary=false ORDER BY order_id",PhotosetID).fetch(1000)
    
	def GetPhotosetTitle(self,PhotosetID):
		return db.GqlQuery("SELECT * FROM Photosets where photoset_id=:1",PhotosetID).get().title