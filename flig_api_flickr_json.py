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

import httplib, urllib, hashlib

try: 
	import json
except ImportError: 
	from django.utils import simplejson as json

class FlickrReqError(Exception):
	"""Исключение порождается при ошибках получения и обработки данных с Flickr"""
	def ___init___(value,message):
		self.value=value
		self.message=message
		
#		10 - Код ответа сервера не равен 200
#		20 - Атрибут status ответа не равен "ok"



class FlickrJSON:
	""" Methods:
	Photos_getSizes(PHOTO_ID)
	Photos_getInfo(PHOTO_ID)
	Photosets_getPhotos(PHOTOSET_ID)
	Photosets_getInfo(PHOTOSET_ID)
	Photosets_getList(USER_ID)
	All methods return Python object
	"""
	
	__g_params={"format":"json"}
	__api_srv="api.flickr.com"
	__api_callpath="/services/rest/"
	

	def __init__(self,AUTH_DATA):
		self.__secret	=	AUTH_DATA["secret"]
		self.__g_params["api_key"]	=	AUTH_DATA["api_key"]
		self.__g_params["auth_token"]	=	AUTH_DATA["auth_token"]
		
	
	def __SendReq(self,method,l_params):
		"""Формирует и отправляет запрос на Flickr и обрабатывает ответ"""
		
		# Формируем подпись запроса
		l_params.update(self.__g_params)
		l_params.update({"method":method})
		
		
		API_SIG_STR=self.__secret
		
		for param in sorted(l_params.keys()):
			API_SIG_STR=API_SIG_STR+param+l_params[param]
		
		hash=hashlib.md5()
		hash.update(API_SIG_STR)
		
		l_params["api_sig"]=hash.hexdigest()
		
		
		
		# Формируем запрос
		REQSTR=self.__api_callpath+"?"
		
		
		for param in sorted(l_params.keys()):
			REQSTR=REQSTR+param+"="+l_params[param]+"&"
		
		
		# По хорошему, убирать бы знак & в конце REQSTR, но работает и с ним 
		REQSTR=REQSTR[:-1]	
		
		# Отправляем запрос и возвращаем ответ
		headers = { "Content-type": "text/xml","Accept": "text/plain"}
	
		conn = httplib.HTTPConnection(self.__api_srv)
		conn.request("GET", REQSTR)
		r = conn.getresponse()
	
		#print r.status, r.reason
		if r.status==200:
			Resp=r.read()
			conn.close()
			#print Resp
			if Resp!=-1:
				ReturnObj=json.loads(Resp[14:-1])
				if ReturnObj[u"stat"]=='ok':
					return ReturnObj
				else:
					raise FlickrReqError(10,"Flickr error: HTTP Error code "+ str(r.status)+Resp)
					return -1
		else:
			raise FlickrReqError(10,r.status)
			return -1
		
		

	def Photos_getSizes(self,PHOTO_ID):
		"""flickr.photos.getSizes"""
		return self.__SendReq("flickr.photos.getSizes",{"photo_id":PHOTO_ID})
	    
	def Photos_getInfo(self, PHOTO_ID):
		"""flickr.photos.getInfo"""
		return self.__SendReq("flickr.photos.getInfo",{"photo_id":PHOTO_ID})	
	
	def Photosets_getPhotos(self, PHOTOSET_ID):
		"""flickr.photosets.getPhotos"""
		return self.__SendReq("flickr.photosets.getPhotos",{"photoset_id":PHOTOSET_ID})
	    
	def Photosets_getInfo(self, PHOTOSET_ID):
		"""flickr.photosets.getInfo"""
		return self.__SendReq("flickr.photosets.getInfo",{"photoset_id":PHOTOSET_ID})
		
	def Photosets_getList(self, USER_ID):
		"""flickr.photosets.getList"""
		return self.__SendReq("flickr.photosets.getList",{"user_id":USER_ID})
	
	def Photosets_orderSets(self, PHOTOSET_IDs):
		"""flickr.photosets.getList"""
		return self.__SendReq("flickr.photosets.orderSets",{"photoset_ids":PHOTOSET_IDs})