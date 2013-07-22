#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from flig_api_flickr_json import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import quota
import datetime
from config import *

class Photosets(db.Model):
    photoset_id = db.StringProperty()
    title = db.StringProperty()
    description = db.StringProperty(multiline=True)
    primary = db.StringProperty()
    order_id = db.IntegerProperty()
    update_id = db.IntegerProperty() 
    
            
class Photos(db.Model):
	photo_id = db.StringProperty()
	order_id = db.IntegerProperty()
	photoset_id = db.StringProperty()
	title = db.StringProperty()
	description = db.StringProperty(multiline=True)
	square_source = db.StringProperty()
	square_width = db.IntegerProperty()
	square_height = db.IntegerProperty()
	thumbnail_source = db.StringProperty()
	thumbnail_width = db.IntegerProperty()
	thumbnail_height = db.IntegerProperty()
	small_source = db.StringProperty()
	small_width = db.IntegerProperty()
	small_height = db.IntegerProperty()
	medium_source = db.StringProperty()
	medium_width = db.IntegerProperty()
	medium_height = db.IntegerProperty()
	large_source = db.StringProperty()
	large_width = db.IntegerProperty()
	large_height = db.IntegerProperty()
	isprimary = db.BooleanProperty()
	update_id = db.IntegerProperty()  
    
def UpdatePhotos(PHOTOSET_ID):


	#start = quota.get_request_cpu_usage()
	#==Получение данных с фликра и их подготовка
	Flk=FlickrJSON(AUTH_DATA)
	#end = quota.get_request_cpu_usage()
	
	#GetData=start-end
	
	#start = quota.get_request_cpu_usage()
	PhotosetPhotos=Flk.Photosets_getPhotos(PHOTOSET_ID)
	
	update_id=datetime.datetime.now().microsecond
	
	PhotoList=[]
	
	order_id=1
	for photos in PhotosetPhotos[u"photoset"][u"photo"]:
        
		PhotoSizes=Flk.Photos_getSizes(photos[u"id"])
		PhotoInfo=Flk.Photos_getInfo(photos[u"id"])
		
		      
		Photo=Photos(key_name=photos[u"id"])
		
		Photo.photo_id = photos[u"id"]
		Photo.order_id = order_id
		Photo.photoset_id = PHOTOSET_ID
		Photo.update_id=update_id
		Photo.title = photos[u"title"]
		Photo.description = PhotoInfo[u"photo"][u"description"]["_content"]
		
		for size in PhotoSizes[u"sizes"][u"size"]:
			if size[u"label"]=="Square":
				Photo.square_source=size[u"source"]
				Photo.square_width=int(size[u"width"])
				Photo.square_height=int(size[u"height"])
			elif size[u"label"]=="Thumbnail":
				Photo.thumbnail_source=size[u"source"]
				Photo.thumbnail_width=int(size[u"width"])
				Photo.thumbnail_height=int(size[u"height"])
			elif size[u"label"]=="Small":
				Photo.small_source=size[u"source"]
				Photo.small_width=int(size[u"width"])
				Photo.small_height=int(size[u"height"])
			elif size[u"label"]=="Medium":
				Photo.medium_source=size[u"source"]
				Photo.medium_width=int(size[u"width"])
				Photo.medium_height=int(size[u"height"])
			elif size[u"label"]=="Large":
				try:
					Photo.large_source=size[u"source"]
					Photo.large_width=int(size[u"width"])     
					Photo.large_height=int(size[u"height"])
				except KeyError:
					Photo.large_source = ""
					Photo.large_width = 0
					Photo.large_height = 0

		Photo.isprimary=bool(int(photos[u"isprimary"]))
		
		if bool(PhotoInfo[u"photo"][u"visibility"][u"ispublic"]) | bool(int(photos[u"isprimary"])):    
		    PhotoList.append(Photo)
		    
		order_id=order_id+1
		
	#end = quota.get_request_cpu_usage()
		    
	#PrepareData=start-end
    
	#WriteData=1
	#DeleteData=1
    
    #== Запись данных    
	if PhotoList:
		
		#start = quota.get_request_cpu_usage()
		db.put(PhotoList)
		#end = quota.get_request_cpu_usage()
		#WriteData=start-end
		
		
		#start = quota.get_request_cpu_usage()
	#Удаление неактуальных данных
		qPhotos= db.GqlQuery("SELECT * FROM Photos where photoset_id=:1 and update_id!=:2")
		qPhotos.bind(PHOTOSET_ID,update_id)
		cPhotos= qPhotos.fetch(1000)
		
		if len(cPhotos)>0:
			db.delete(cPhotos)
		#end = quota.get_request_cpu_usage()
		
		#DeleteData=start-end
		
				    
	else:
	    return "Error in processing Flickr data"

	return "ok"
	#return "GetData: "+str(GetData)+"<br>\nPrepareData: "+str(PrepareData)+"<br>\nWriteData: "+str(WriteData)+"<br>\nDeleteData: "+str(DeleteData)

    
   
def UpdatePhotosets(USER_ID):
	
	
	Flk=FlickrJSON(AUTH_DATA)
	
	FPhotosetList=Flk.Photosets_getList(USER_ID)[u"photosets"][u"photoset"]
	
	update_id=datetime.datetime.now().microsecond
	PhotosetList=[]
	
	if FPhotosetList:
		
	# Подготовка данных
		order_id=1
		for FListItem in FPhotosetList:
			Photoset = Photosets(key_name=FListItem[u"id"])			

			Photoset.photoset_id=FListItem[u"id"]
			Photoset.update_id=update_id
			Photoset.title=FListItem[u"title"][u"_content"]
			Photoset.description=FListItem[u"description"][u"_content"]
			Photoset.primary=FListItem[u"primary"]
			Photoset.order_id=order_id
			
			PhotosetList.append(Photoset)
			
			order_id=order_id+1
	

		# Запись данных
		db.put(PhotosetList)
			
		# Удаление неактуальных записей
		qPhotosets= db.GqlQuery("SELECT * FROM Photosets WHERE update_id!=:1")
		qPhotosets.bind(update_id)
		cPhotosets= qPhotosets.fetch(1000)
		
		if len(cPhotosets)>0:
			db.delete(cPhotosets)
		
		
	else:
	    return "Error in processing Flickr data"
			  
	return "ok"
   
    