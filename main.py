#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import webapp2
from flig_web_ui_main import UI_Main
from flig_web_wrk import WRK_UpdateGal
from sitemap import Sitemap
from flig_web_ui_photoset import UI_Photoset

application = webapp2.WSGIApplication([('/', UI_Main),
									  ('/update_gal', WRK_UpdateGal),
									  ('/photoset', UI_Photoset),
									  ('/sitemap.xml',Sitemap)
									],
                                     debug=True)