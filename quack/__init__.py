"""
Copyright 2017 Deepgram
"""

import logging

TRACE_LEVEL = 5
def _trace(self, message, *args, **kwargs):
	""" Writes a trace-level message to the log.
	"""
	if self.isEnabledFor(TRACE_LEVEL):
		# pylint: disable=protected-access
		self._log(TRACE_LEVEL, message, args, **kwargs)
		# pylint: enable=protected-access

logging.addLevelName(TRACE_LEVEL, 'TRACE')
logging.TRACE = TRACE_LEVEL
logging.Logger.trace = _trace

# pylint: disable=wrong-import-position,wildcard-import
from .version import __version__
from .exceptions import *
from .aspects import aspect
from .routes import route, get_routes, Handler
from .server import create_server
# pylint: enable=wrong-import-position,wildcard-import

### EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF
