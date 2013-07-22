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

class UIMain(webapp2.RequestHandler):
	def get(self):
		template_values = {
			"Photosets": self.get_photosets_blocks(4),
			"GetPhotoset_url":"/photoset?id=",
			"RefreshLink":""
			}
		
		CUser = users.get_current_user()
		if CUser:
			if users.is_current_user_admin():
				template_values["RefreshLink"] = "<a href='/update_gal'> Refresh</a>"
			else:
				template_values["RefreshLink"] = ""
		else:
			template_values["RefreshLink"] = "".join(["<a class='admin_refresh' href='",users.create_login_url(self.request.uri),"'> *</a>"])    
		
		template = JINJA_ENVIRONMENT.get_template('templates/ui_main.html')
		self.response.write(template.render(template_values))
        
	def get_photosets_blocks(self,block_size):
	   	photosets = []
	   	photoset_block = []
	   	b = bc = 1
	   	photosets.append({"Block_content":photoset_block,"Block_id":bc})
		
		photosets_query = db.GqlQuery("SELECT * FROM Photosets ORDER BY order_id")
		photo_query =  db.GqlQuery("SELECT * FROM Photos where photo_id=:1")

		for stored_photoset in photosets_query:
			photoset = {}
			photoset["title"] = stored_photoset.title
			photoset["photoset_id"] = stored_photoset.photoset_id
			photoset["order_id"] = stored_photoset.order_id
	    	
			photo_query.bind(stored_photoset.primary)
			
			for photo in photo_query:
				photoset["thumbnail_url"] = photo.small_source
				photoset["thumbnail_width"] = photo.small_width
				photoset["thumbnail_height"] = photo.small_height
			
			photoset_block.append(photoset)
			
			if b >= 4:
				b = 0
				bc = bc+1
				photoset_block = []
				photosets.append({"Block_content":photoset_block,"Block_id":bc})
			
			b = b+1
		return photosets