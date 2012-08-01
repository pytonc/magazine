
import json

from google.appengine.ext import ndb

from models import Articles
from lib.utils import login_required, slugify, valid_slug
from lib.basehandler import BaseHandler
from utils import *


class ArticleList(BaseHandler):
    """ Outputs a list of articles """
    def get(self):
        # TODO: Remove cached_time
        articles, cached_time = get_articles()
        if cached_time:
            cached_time = datetime.datetime.now() - cached_time
            cached_time = int(cached_time.total_seconds())
        else:
            cached_time = 0
        self.render('articles/articles.html', articles=articles, cached_time=cached_time, logged_in=self.current_user)


class ArticleListJson(BaseHandler):
    """ Outputs a list of articles in json format """
    # TODO: merge this class with ArticleList
    def get(self):
        posts = get_articles()[0]  # returns a tuple (posts, cache_time)
        content = [{
                    'subject': post.title,
                    'content': post.post,
                    'created': str(post.created.strftime('%a %b %d %H:%M:%S %Y')),
                    'last_modified': str(post.last_modified.strftime('%a %b %d %H:%M:%S %Y'))
                   }
                   for post in posts]
        self.response.headers['Content-Type'] = 'application/json'
        self.write(json.dumps(content))


class Article(BaseHandler):
    """ Single article handler """

    def get(self, slug=''):
        if slug:
            # TODO: remove cached_time
            content, cached_time = get_article(slug)
            if content:
                logged_in = self.current_user
                if cached_time:
                    cached_time = datetime.datetime.now() - cached_time
                    cached_time = int(cached_time.total_seconds())
                else:
                    cached_time = 0
                self.render('articles/article.html', post=content, logged_in=logged_in, cached_time=cached_time)
            else:
                self.error(404)
        else:
            self.error(404)


class ArticleJson(BaseHandler):
    # TODO: merge this class with Article
    def get(self, slug):
        if slug:
            content, cache_time = get_article(slug)
            if content:
                content = {'subject': content.title,
                           'content': content.post,
                           'created': str(content.created.strftime('%a %b %d %H:%M:%S %Y')),
                           'last_modified': str(content.last_modified.strftime('%a %b %d %H:%M:%S %Y'))}
                self.response.headers['Content-Type'] = 'application/json'
                self.write(json.dumps(content))
            else:
                self.error(404)
        else:
            self.error(404)


class ArticleSubmit(BaseHandler):

    def render_post(self, title='', post='', slug='', error='', logged_in=''):
        self.render('blog/submit.html', title=title, post=post, slug=slug, error=error, logged_in=logged_in)

    @login_required
    def get(self):
        self.render_post(logged_in=True)

    @login_required
    def post(self):
        title = self.request.get('subject')
        post = self.request.get('content')
        slug = self.request.get('slug')

        error = dict()

        if title and post:
            if not slug:
                slug = slugify(str(title))
            slug_in_db = Articles.ll().filter('slug =', slug).get()

            if not slug_in_db:
                submission = Articles(title=title, post=post, slug=slug)
                submission.put()

                memcache.flush_all()

            else:
                error['slug'] = 'Sorry, this slug is taken. Please enter a unique one'
                self.render_post(title, post, slug, error)
        else:
            if not title:
                error['subject'] = 'Please enter a title'
            if not post:
                error['post'] = 'Please enter some content'
            self.render_post(title, post, slug, error)


class EditHandler(BaseHandler):
    @login_required
    def render_form(self, form):
        self.render('articles/edit.html', form=form)

    @login_required
    def post(self):
        title = self.request.get('subject')
        post = self.request.get('content')
        slug = self.request.get('slug')
        cid = self.request.get('cid')

        error = dict()
        cid = int(cid)
        if title and post:
            if not slug or not valid_slug(slug):
                slug = slugify(str(title))
            slug_in_db = Articles.all().filter('slug =', slug).get()

            if not slug_in_db or cid == slug_in_db.key().id():
                edit = Articles.get_by_id(cid)
                edit.title = title
                edit.post = post
                edit.slug = slug
                edit.put()

                # Remove from memcache
                memcache.flush_all()
                self.redirect('/articles/' + slug)

            else:
                error['slug'] = 'Sorry, this slug is taken. Please enter a unique one'
                form = {'title': title, 'post': post, 'slug': slug, 'cid': cid, 'error': error, 'logged_in': True}
                self.render_form(form)
        else:
            if not title:
                error['subject'] = 'Please enter a title'
            if not post:
                error['post'] = 'Please enter some content'
            form = {'title': title, 'post': post, 'slug': slug, 'cid': cid, 'error': error, 'logged_in': True}
            self.render_form(form)


class ArticleDelete(BaseHandler):

    @login_required
    def post(self):
        slug = self.request.get('slug')
        if slug:
            article = get_article(slug)[0]  # returns a tuple of posts, cache_time
            if article:
                ndb.delete(article)
                memcache.flush_all()
                self.render('articles/_deleted.html')  # A html fragment returned via ajax


class FlushCacheHandler(BaseHandler):

    @login_required
    def get(self):
        memcache.flush_all()
        self.redirect_to('articles')
