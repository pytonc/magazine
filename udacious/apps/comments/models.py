

from google.appengine.ext import ndb

# ideally, there will be a class for both individual comments, 
# and all the comments for a particular URL together and in order

class Comment(ndb.Model):
    """ individual comment """
    content = ndb.StringProperty(required = True)
    user_id = ndb.KeyProperty(Kind = User)
    created = ndb.DateTimeProperty(auto_now_add = True)
    parent_id = ndb.IntegerProperty(required = False)
    url = ndb.StringProperty(required = True)

    @classmethod
    def comments_by_url(cls, _url, _limit):
    	comments = Comment.query().filter(cls.url == _url, ndb.AND(parent_id = None)).order(+created).fetch(_limit)
    	if comments:
    		return comments
    	return None

    @classmethod
    def child_comments(cls, _parent_id, _limit):
    	child = Comment.query().filter(cls.parent_id == _parent_id).order(+created).fetch(_limit)
    	if child:
    		return child
    	return None

    @classmethod
    def user_comments(cls, _user, _limit):
    	usr_comments = Comment.query().filter(cls.user_id == _user).order(+created).fetch(_limit)
    	if usr_comments:
    		return usr_comments
    	else:
    		return None