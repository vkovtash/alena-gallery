#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import webapp2
from flig_web_ui_main import UIMain
from flig_web_wrk import WRKUpdateGal
from flig_web_ui_photoset import UIPhotoset
from sitemap import Sitemap

application = webapp2.WSGIApplication([('/', UIMain),
									  ('/update_gal', WRKUpdateGal),
									  ('/photoset', UIPhotoset),
									  ('/sitemap.xml',Sitemap)
									],
                                     debug=True)