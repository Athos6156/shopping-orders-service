import logging


class LoggingMiddleware:

	def __init__(self, app):
		self.app=app

	def __call__(self, environ, start_response):
		logging.info(f"Incoming request: {environ['PATH_INFO']}")
		return self.app(environ, start_response)

