import json

from google.appengine.ext import ndb

from lib.utils import login_required, slugify, valid_slug
from lib.basehandler import BaseHandler
from models import import Comment

def get_comments_by_url(url, limit=10, json=False):
    ''' returns an array of comments (or None) related to url '''
    # How to deal with nested comments?
    return

def add_comment(url, user_id, content, parent=None):
    ''' add a comment to the url '''
    return
    
def get_comments_by_user(user_id, limit=10, json=False):
    return

def get_child_comments(parent_id, limit=10, json=False):
    return