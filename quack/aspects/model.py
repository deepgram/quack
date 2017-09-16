"""
Copyright 2017 Deepgram
"""

import datetime
import json

from . import aspect

###############################################################################
class JSONRenderer:					# pylint: disable=too-few-public-methods
	""" Class which renders JSON blobs.
	"""

	###########################################################################
	def __init__(self, pretty):
		""" Creates a new JSON renderer.

			Arguments
			---------

			pretty: bool. Whether or not to render pretty-printed JSON.
		"""
		super().__init__()
		self.pretty = pretty

	###########################################################################
	@staticmethod
	def _handler(value):
		""" Custom JSON serializer for handling ``datetime`` types.
		"""
		if isinstance(value, datetime.datetime):
			return str(value)
		raise ValueError('Cannot render unknown JSON type: {}'.format(
			type(value)))

	###########################################################################
	def render(self, data):
		""" Renders JSON-serializable data.
		"""
		kwargs = {
			'default' : self._handler
		}
		if self.pretty:
			kwargs.update({
				'sort_keys' : True,
				'indent' : 4,
				'separators' : (',', ': ')
			})
		return json.dumps(data, **kwargs)

###############################################################################
aspect.constant('model_renderer', JSONRenderer(pretty=False))

### EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF
