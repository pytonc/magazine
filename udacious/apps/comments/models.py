

from google.appengine.ext import ndb

# ideally, there will be a class for both individual comments, 
# and all the comments for a particular URL together and in order

class Comment(ndb.Model):
    """ individual comment """
    content = ndb.StringProperty(required = True)
    user_id = ndb.IntegerProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    parent_id = ndb.IntegerProperty(required = False) 