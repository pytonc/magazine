
from google.appengine.ext import ndb
class Article(ndb.Model):
    author = ndb.StringProperty(required = True)
    article_title = ndb.StringProperty(required = True)
    content = ndb.TextProperty(required = True)
    # Added for testing (tags)
    # Will this be a separate app?
    tags = ndb.StringProperty(repeated = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now_add = True)
    # Added for testing (rating)
    # Will this be a separate app?
    rating = ndb.FloatProperty(required = True)
    
    @classmethod
    def single_article(cls, _user, _title):
        result = Article.query().filter(cls.author == _user).filter(cls.article_title == _title).get()
        return result
    
    @classmethod
    def rate_article(cls):
        # TBD needs implemented
        d = timedelta(days = 7)
        if datetime.date() > cls.created + d:
            rating = cls.rating * 1.01
        else:
            rating = cls.rating * 1.15
        cls.put()
        return rating

    @classmethod
    def by_date(cls, n):
        result = Article.query().order(-cls.created).fetch(n)
        return result

    @classmethod
    def by_rating(cls, n):
    	result = Article.query().order(-cls.rating).fetch(n)
    	return result

    @classmethod
    def by_tag(cls, _tag):
        # TBD Re-work this for tag model
    	result = Article.query().filter(cls.tags == _tag).fetch(10)
    	return result

    @classmethod
    def by_author(cls, _author):
        # TBD add this feature to handlers
    	result = Article.query().filter(cls.author == _author).fetch(10)
    	return result