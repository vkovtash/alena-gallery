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


class UI_Main(webapp.RequestHandler):
	def get(self):
    
		#==Обработать Ошибку
		Tmain_values = {
			"Photosets": self.GetPhotosetsBlocks(4),
			"GetPhotoset_url":"/photoset?id=",
			"RefreshLink":""
			}
		
		
		CUser = users.get_current_user()
		if CUser:
			if users.is_current_user_admin():
				Tmain_values["RefreshLink"]="<a href='/update_gal?photoset_id=1111111111'> Refresh</a>"
			else:
				Tmain_values["RefreshLink"]=""
		else:
			Tmain_values["RefreshLink"]="<a class='admin_refresh' href='"+users.create_login_url(self.request.uri)+"'> *</a>"    
		
		path = os.path.join(os.path.dirname(__file__), 'templates/ui_main.html')
		self.response.out.write(template.render(path, Tmain_values))	
        
	def GetPhotosetsBlocks(self,block_size):
	   	Photosets = []
	   	Photoset_block=[]
	   	b=bc=1
		
		QPhotosets = db.GqlQuery("SELECT * FROM Photosets ORDER BY order_id")
		QPhoto =  db.GqlQuery("SELECT * FROM Photos where photo_id=:1")
		
		for QPhotoset in QPhotosets:
			Photoset = {}
			Photoset["title"] = QPhotoset.title
			Photoset["photoset_id"]= QPhotoset.photoset_id
			Photoset["order_id"]=QPhotoset.order_id
	    	
			QPhoto.bind(QPhotoset.primary)
			
			for photo in QPhoto:
				
				Photoset["thumbnail_url"]=photo.small_source
				Photoset["thumbnail_width"]=photo.small_width
				Photoset["thumbnail_height"]=photo.small_height
			
			
			Photoset_block.append(Photoset)
			
			if b>=4:
				Photosets.append({"Block_content":Photoset_block,"Block_id":bc})
				b=0
				bc=bc+1
				Photoset_block=[]
			
			b=b+1
	    
		return Photosets