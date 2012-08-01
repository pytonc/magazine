import logging
import datetime

from google.appengine.api import memcache

from models import Articles


def get_articles(count=10, update=False):
    ''' Adding to and Retrieving from memcache '''
    key = 'top_' + str(count)
    value = memcache.get(key)
    if value is None or update:
        logging.info('Ran a query to retrieve the top posts')
        posts = Articles.query().order(-Articles.created).fetch(count)
        value = (list(posts), datetime.datetime.now())
        memcache.set(key, value)
    return value


def get_article(slug, update=False):
    ''' Caching single article objects. Used by Article, JsonArticle, and Delete '''
    key = slug
    value = memcache.get(key)

    if value is None or update:
        logging.info('Ran a query to retrive an article')
        post = Articles.query().filter('slug =', key).get()
        if post:
            value = (post, datetime.datetime.now())
            memcache.set(key, value)
        else:
            return (None, None)
    return value
