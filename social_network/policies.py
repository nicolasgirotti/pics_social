from social_network import app


class CSPMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            headers.append(('Content-Security-Policy', 'default-src \'self\''))
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)

class XFOMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            headers.append(('X-Frame-Options', 'SAMEORIGIN'))
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)

class HSTSMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            headers.append(('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload'))
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)

def add_middlewares(app):
    app.wsgi_app = CSPMiddleware(XFOMiddleware(HSTSMiddleware(app.wsgi_app)))

add_middlewares(app)