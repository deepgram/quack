"""
Copyright 2017 Deepgram
"""

import base64
import binascii

from . import aspect

###############################################################################
@aspect.dynamic()
def basic_auth_headers(self):
	""" An aspect which extracts the basic authentication information as a
		(username, password) tuple if present, or None if the authentication
		information is missing or malformed.
	"""
	header = self.request.headers.get('Authorization', None)
	if not header:
		return None

	tag = 'Basic '
	if tag not in header:
		return None

	parts = header.split(tag, 1)
	if len(parts) != 2:
		return None

	header = parts[1]
	try:
		header = base64.b64decode(header).decode('utf-8')
		username, password = header.split(':', 1)
	except (binascii.Error, UnicodeDecodeError, ValueError):
		return None

	return (username, password)

### EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF
