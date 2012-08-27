import json
from google.appengine.ext import ndb
from lib.utils import login_required, slugify, valid_slug
from lib.basehandler import BaseHandler
import models


def get_comments_by_url(url, limit=10, json=False):
    ''' returns an array of comments (or None) related to url '''
    comments = Comment.comments_by_url(url, limit)
    # TBD re-factor this functionality.
    nested_comments = []
    if comments:
    	for comment in comments:
    		nested_comments.append(comment)
    		child_comments = get_child_comments(int(comment.key.id()))
    		if child_comments:
    			nested_comments.append(child_comments)
	if not json:
	    return nested_comments    
    return json.dumps(nested_comments)


def add_comment(url, user_id, content, parent=None):
    ''' add a comment to the url '''
    return

    
def get_comments_by_user(user_id, limit=10, json=False):
	''' Returns a list or json array of comments by the user '''
	user_comments = Comment.user_comments(user_id, limit)
    nested_comments = []
    if comments:
    	for comment in user_comments:
    		nested_comments.append(comment)
    		child_comments = get_child_comments(int(comment.key.id()))
    		if child_comments:
    			nested_comments.append(child_comments)
	if not json:
	    return nested_comments    
    return json.dumps(nested_comments)


def get_child_comments(parent_id, limit=10, json=False):
	''' Returns a list of child comments to the calling function.'''
		children = Comment.child_comments(parent_id)
		if children:
			return children
		else:
			return
