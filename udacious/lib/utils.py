import re

USERNAME_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
PASSWORD_RE = re.compile(r'^.{3,20}$')
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
SLUG_RE = re.compile(r'^[a-z0-9-]$')


def valid_username(username):
    ''' checks if a username is of the valid format (else returns None)'''
    return USERNAME_RE.match(username)


def valid_password(password):
    ''' checks if a password is of the valid format (else returns None)'''
    return PASSWORD_RE.match(password)


def valid_email(email):
    ''' checks if email is of the valid format (else returns None)'''
    try:
        return EMAIL_RE.match(email)
    except TypeError:
        return None


def valid_slug(slug):
    ''' checks if slug is of the valid format (else returns None)'''
    return SLUG_RE.match(slug)


def slugify(s):
    ''' converts s to slug'''
    import unicodedata
    if type(s) == unicode:
        s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    s = unicode(re.sub('[^\w\s-]', '', s).strip().lower())
    return re.sub('[-\s]+', '-', s)


def escape_html(s):
    ''' returns HTML-escaped s'''
    import cgi
    return cgi.escape(unicode(s), quote=True).encode('ascii', 'xmlcharrefreplace')


def salt():
    ''' returns salt '''
    import random
    import string
    return ''.join(random.sample(string.letters + string.digits, 5))


def hasher(s, salt):
    ''' given a string and salt, returns a hash '''
    import hashlib
    import hmac
    return hmac.new(salt, s, hashlib.sha256).hexdigest()


def login_required(function):
    ''' This is a decorator that checks whether a user is logged in '''
    def _f(self, *args, **kwargs):
        if self.current_user:
            function(self, *args, **kwargs)
        else:
            # next_page = self.request.path
            self.redirect_to('login')
    return _f
