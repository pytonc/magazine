#!/usr/bin/env python
##
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

import os

from webapp2 import WSGIApplication
from webapp2_extras.routes import RedirectRoute, PathPrefixRoute

# Set useful fields
root_dir = os.path.dirname(__file__)
template_dir = os.path.join(root_dir, 'templates')

# Create the WSGI application and define route handlers
app = WSGIApplication(
    [
        PathPrefixRoute('/articles', [
            RedirectRoute('/', handler='apps.articles.handlers.ArticleList', name='articles', strict_slash=False),
            RedirectRoute('/.json', handler='apps.articles.handlers.ArticleListJson', name='articles_json', strict_slash=True),
            RedirectRoute(r'/<slug:[-\w]+>', handler='apps.articles.handlers.Article'),
            RedirectRoute(r'/<slug:[-\w]+>.json', handler='apps.articles.handlers.ArticleJson'),
        ]),
        PathPrefixRoute('/profile', [
            RedirectRoute(r'/<slug:[-\w]+>', handler='apps.profiles.handlers.Profile'),
            RedirectRoute(r'/<slug:[-\w]+>/edit', handler='apps.profiles.handlers.EditProfile'),
        ]),
        PathPrefixRoute('/user', [
            RedirectRoute('/signup', handler='apps.user.handlers.Signup', name='signup', strict_slash=True),
            RedirectRoute('/login', handler='apps.user.handlers.Login', name='login', strict_slash=True),
            RedirectRoute('/logout', handler='apps.user.handlers.Logout', name='logout', strict_slash=True),
        ]),
        PathPrefixRoute('/admin', [
            RedirectRoute('/flush', handler='apps.admin.handlers.FlushCacheHandler', name='flush_memcache'),
        ]),
    ], debug=True)
