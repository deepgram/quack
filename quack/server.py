import logging

from tornado.ioloop import IOLoop
from tornado.platform.asyncio import AsyncIOMainLoop
import tornado.web
import tornado.httpserver

from . import get_routes

logger = logging.getLogger(__name__)

###############################################################################
def create_server(port=8080, base_url=None, max_buffer_size=10*1024*1024, debug=False):
	""" Run the main event loop.

		Examples
		--------

		.. code-block:: python

			import asyncio
			from quack import create_server, route, aspect, Handler, \
				Http401Unauthorized

			@route('/test')
			class TestHandler(Handler):

				@aspect('basic_auth_headers')
				async def _get(self, basic_auth_headers=None):
					if basic_auth_headers is None:
						raise Http401Unauthorized({
							'result' : 'failure',
							'reason' : 'No basic authentication headers.'
						})
					return {'user' : basic_auth_headers[0]}

			create_server()
			asyncio.get_event_loop().run_forever()
	"""
	if not IOLoop.initialized():
		logger.debug('Installing the Tornado IOLoop.')
		AsyncIOMainLoop().install()

	app = tornado.web.Application(
		get_routes(base_url),
		debug=debug
	)
	server = tornado.httpserver.HTTPServer(app, max_buffer_size=max_buffer_size)
	server.listen(port)

	return server
