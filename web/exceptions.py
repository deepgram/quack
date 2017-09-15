"""
Copyright 2017 Deepgram
"""

###############################################################################
class HttpException(Exception):
	""" Base class for all HTTP exceptions.
	"""

	###########################################################################
	def __init__(self, response=None, *args, code=None, headers=None,
		**kwargs):
		""" Creates a new exception instance. This is provided so that the code
			can be specified on-the-fly rather than needing a derived class.
		"""
		super().__init__(*args, **kwargs)

		if code is not None:
			self.code = code

		if headers is not None:
			assert isinstance(headers, dict)
			self.headers = headers
		elif not hasattr(self, 'headers'):
			self.headers = {}

		self.response = response

###############################################################################
def make_class(name, code, *, headers=None):
	""" Creates a new exception class with a given HTTP code.
	"""
	kwargs = {'code' : code}
	if headers:
		assert isinstance(headers, dict)
		kwargs['headers'] = headers
	return type(name, (HttpException, ), kwargs)

###############################################################################
# Common exception classes

# pylint: disable=invalid-name
Http400BadRequest = make_class('Http400BadRequest', 400)
Http401Unauthorized = make_class('Http401Unauthorized', 401,
	headers={'WWW-Authenticate' : 'Basic realm=Restricted'})
Http403Forbidden = make_class('Http403Forbidden', 403)
Http404NotFound = make_class('Http404NotFound', 404)
Http405MethodNotAllowed = make_class('Http405MethodNotAllowed', 405)
Http409Conflict = make_class('Http409Conflict', 409)

Http500InternalServerError = make_class('Http500InternalServerError', 500)
Http501NotImplemented = make_class('Http501NotImplemented', 501)
Http503ServiceUnavailable = make_class('Http503ServiceUnavailable', 503)
# pylint: enable=invalid-name

### EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF
