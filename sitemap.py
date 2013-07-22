#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import db

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


class Sitemap(webapp2.RequestHandler):
	def get(self):
		Tmain_values = {
			"Photosets": self.GetPhotosets(),
			"GetPhotoset_url":"/photoset?id=",
			"RefreshLink":""
			}
		
		template = JINJA_ENVIRONMENT.get_template('templates/sitemap.xml')
		self.response.write(template.render(Tmain_values))
        
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