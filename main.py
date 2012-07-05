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


from flig_web_ui_main import UI_Main
from flig_web_wrk import WRK_UpdateGal
from flig_web_ui_cpanel import UI_CPanel
from sitemap import Sitemap
from flig_web_ui_photoset import UI_Photoset
from google.appengine.ext.webapp import util
from google.appengine.ext import webapp

def main():
    application = webapp.WSGIApplication([('/', UI_Main),
    									  ('/update_gal', WRK_UpdateGal),
    									  ('/photoset', UI_Photoset),
    									  ('/sitemap.xml',Sitemap)
#    									  ('/cpanel', UI_CPanel)
										],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
