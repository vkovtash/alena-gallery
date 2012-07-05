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


class Sitemap(webapp.RequestHandler):
	def get(self):
    
		#==Обработать Ошибку
		Tmain_values = {
			"Photosets": self.GetPhotosets(),
			"GetPhotoset_url":"/photoset?id=",
			"RefreshLink":""
			}
		  
		
		path = os.path.join(os.path.dirname(__file__), 'templates/sitemap.xml')
		self.response.out.write(template.render(path, Tmain_values))	
        
	def GetPhotosets(self):
	   	Photosets = []
		
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
			
			
			Photosets.append(Photoset)
			
		return Photosets