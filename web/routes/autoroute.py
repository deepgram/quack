"""
Copyright 2017 Deepgram
"""

import re
import logging

from tornado.web import RequestHandler

from .. import aspect, HttpException, Http405MethodNotAllowed

logger = logging.getLogger(__name__)

###############################################################################
class Handler:						# pylint: disable=too-few-public-methods
	""" The base class for all endpoint handlers.

		This is intended to be used with ``@route``, as in:

		.. code-block:: python

			@route('/my-endpoint')
			class MyEndpoint(Handler):
				async def _get(self, *args, **kwargs):
					# Handle GET requests
					pass

		The reason for having this base class is twofold:

		1. It logically separates Tornado-required boilerplate and exception
		   handling, which has been relegated to the ``AutoHandler`` class
		   below.
		2. The ``AutoHandler`` instance is the actual class that it is
		   presented to Tornado as a request handler. But ``AutoHandler``
		   inherits from the class that is decorated with ``@route``. This
		   creates an inverted class hierarchy. Putting in
		   ``NotImplementedError`` function stubs (abstract methods) into
		   ``AutoHandler`` no longer makes sense, since it is at the **end** of
		   the inheritance tree. We could instead enforce abstract methods by
		   convenient/documentation, or we could check (using reflection) which
		   methods are actually available on the instantiated class (e.g.,
		   ``hasattr(self, '_get')``), but by far the easiest and cleanest way
		   to do this is to provide a second base class that stubs out the
		   optional/required methods that endpoint handlers can implement.
	"""

	# pylint: disable=no-self-use,unused-argument

	#######################################################################
	async def _get(self, *args, **kwargs):
		""" Implementation of the GET handler.
		"""
		raise Http405MethodNotAllowed

	#######################################################################
	async def _post(self, *args, **kwargs):
		""" Implementation of the POST handler.
		"""
		raise Http405MethodNotAllowed

	#######################################################################
	async def _put(self, *args, **kwargs):
		""" Implementation of the PUT handler.
		"""
		raise Http405MethodNotAllowed

	#######################################################################
	async def _delete(self, *args, **kwargs):
		""" Implementation of the DELETE handler.
		"""
		raise Http405MethodNotAllowed

	# pylint: enable=no-self-use,unused-argument

###############################################################################
def _create_tornado_handler(handler_class):
	""" Creates a new Tornado request handler.
	"""

	###########################################################################
	class AutoHandler(RequestHandler, handler_class): # pylint: disable=abstract-method
		""" Magically created Tornado handler.
		"""

		#######################################################################
		def set_default_headers(self):
			""" Sets the default headers.
			"""
			self.set_header('Access-Control-Allow-Origin', '*')
			self.set_header('Access-Control-Allow-Headers', ', '.join([
				'authorization', 'Authorization', 'Content-Type', 'Depth',
				'User-Agent', 'X-File-Size', 'X-Requested-With',
				'X-Requested-By', 'If-Modified-Since', 'X-File-Name',
				'Cache-Control'
			]))
			self.set_header('Access-Control-Allow-Methods', ', '.join([
				'PUT', 'DELETE', 'POST', 'GET', 'OPTIONS'
			]))

		#######################################################################
		def options(self, *args, **kwargs):
			""" Responds to an OPTIONS request.
			"""
			self.set_status(204)
			self.finish()

		#######################################################################
		@aspect('model_renderer')
		def render_data(self, data, model_renderer=None):
			""" Renders data.
			"""
			return model_renderer.render(data)

		#######################################################################
		async def _handle(self, func, *args, **kwargs):
			""" Handler for all requests.
			"""
			try:
				result = await func(*args, **kwargs)
				self.write(self.render_data(result))
			except HttpException as exception:
				for k, v in exception.headers.items():
					self.set_header(k, v)
				self.set_status(exception.code)
				if exception.response:
					self.finish(self.render_data(exception.response))
			except:								# pylint: disable=bare-except
				logger.exception('Failed to handle request.')
				self.set_status(500)

		#######################################################################
		async def get(self, *args, **kwargs):
			""" Handle a GET request.
			"""
			return (await self._handle(self._get, *args, **kwargs))

		#######################################################################
		async def post(self, *args, **kwargs):
			""" Handle a POST request.
			"""
			return (await self._handle(self._post, *args, **kwargs))

		#######################################################################
		async def put(self, *args, **kwargs):
			""" Handle a PUT request.
			"""
			return (await self._handle(self._put, *args, **kwargs))

		#######################################################################
		async def delete(self, *args, **kwargs):
			""" Handle a DELETE request.
			"""
			return (await self._handle(self._delete, *args, **kwargs))

	return AutoHandler

###############################################################################
def get_routes(prefix=None):
	""" Gets the list of all Tornado routes / endpoints that have been
		registered.

		Arguments
		---------

		prefix: str (default: None). The base URL to prefix all endpoints with.
	"""
	return {
		('{}{}'.format(prefix or '', route), _create_tornado_handler(handler))
		for route, handler in get_routes.routes
	}
get_routes.routes = []

###############################################################################
def _get_param_string(param, valid_type):
	""" Formats a regex capture group.
	"""
	return '(?P<{}>{}+?)'.format(param, r'\d' if valid_type == 'int' else '.')

###############################################################################
def route(url=None, regexp=None):
	""" Registers a route / endpoint.
	"""
	if url is None and regexp is None:
		raise ValueError('Must supply either url or regexp')
	if (url is None) == (regexp is None):
		raise ValueError('Must supply either url or regexp, not both')

	if url:
		for match in route.param_re.finditer(url):
			x = match.groupdict()
			url = url.replace(
				match.group(0),
				_get_param_string(x['param'], x['type'])
			)
	else:
		url = regexp

	###########################################################################
	def decorator(cls):
		""" Registers the route.
		"""
		get_routes.routes.append((url, cls))
		return cls
	return decorator

route.param_re = re.compile(r'<(?P<param>.+?):(?P<type>.+?)>')

### EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF
