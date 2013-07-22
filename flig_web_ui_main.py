#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import db
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class UI_Main(webapp2.RequestHandler):
	def get(self):
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
		
		template = JINJA_ENVIRONMENT.get_template('templates/ui_main.html')
		self.response.write(template.render(Tmain_values))
        
	def GetPhotosetsBlocks(self,block_size):
	   	Photosets = []
	   	Photoset_block = []
	   	b = bc = 1
	   	Photosets.append({"Block_content":Photoset_block,"Block_id":bc})
		
		QPhotosets = db.GqlQuery("SELECT * FROM Photosets ORDER BY order_id")
		QPhoto =  db.GqlQuery("SELECT * FROM Photos where photo_id=:1")

		for QPhotoset in QPhotosets:
			Photoset = {}
			Photoset["title"] = QPhotoset.title
			Photoset["photoset_id"] = QPhotoset.photoset_id
			Photoset["order_id"] = QPhotoset.order_id
	    	
			QPhoto.bind(QPhotoset.primary)
			
			for photo in QPhoto:
				Photoset["thumbnail_url"] = photo.small_source
				Photoset["thumbnail_width"] = photo.small_width
				Photoset["thumbnail_height"] = photo.small_height
			
			Photoset_block.append(Photoset)
			
			if b >= 4:
				b = 0
				bc = bc+1
				Photoset_block = []
				Photosets.append({"Block_content":Photoset_block,"Block_id":bc})
			
			b = b+1
	    
		return Photosets