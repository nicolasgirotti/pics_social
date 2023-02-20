from flask import session, request, abort
from social_network import app
import os



def csrf_protection(app):
    @app.before_request
    def csrf_protect():
        if request.method == "POST":
            token = session.pop('_csrf_token', None)
            if not token or token != request.form.get('_csrf_token'):
                abort(403)

    def generate_csrf_token():
        if '_csrf_token' not in session:
            session['_csrf_token'] = os.urandom(16).hex()
        return session['_csrf_token']

    app.jinja_env.globals['csrf_token'] = generate_csrf_token
    
    
class CSPMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            headers.append(('Content-Security-Policy', 'default-src \'self\''))
            print("CSPM en ejecucion..")
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)

class XFOMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            print("XFO en ejecucion..")
            headers.append(('X-Frame-Options', 'SAMEORIGIN'))
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)

class HSTSMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            print("Hsts en ejecucion..")
            headers.append(('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload'))
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)

def add_middlewares(app):
    app.wsgi_app = CSPMiddleware(XFOMiddleware(HSTSMiddleware(app.wsgi_app)))


add_middlewares(app)