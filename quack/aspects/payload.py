import re
import json
import logging

from ..exceptions import Http400BadRequest
from . import aspect

logger = logging.getLogger(__name__)

def decode_json(body, strict=False, content_type=None):
	try:
		data = json.loads(body.decode('utf-8'))
		return 'application/json', data
	except (UnicodeDecodeError, json.decoder.JSONDecodeError):
		if strict:
			raise Http400BadRequest({
				'result' : 'failure',
				'reason' : 'Bad JSON submitted.'
			})
		return content_type, body

@aspect.dynamic()
def payload(self):
	assert hasattr(self, 'request')

	if 'Content-Type' not in self.request.headers:
		return None

	content_type = self.request.headers['Content-Type']
	body = self.request.body

	assert isinstance(body, bytes)

	if 'application/octet-stream' in content_type:
		return 'application/octet-stream', body
	elif re.match(r'audio/.*', content_type):
		return content_type.split(';')[0], body
	elif re.match(r'video/.*', content_type):
		return content_type.split(';')[0], body
	elif 'multipart/form-data' in content_type:
		if len(self.request.files) != 1:
			raise Http400BadRequest

		file_info = list(self.request.files.items())[0][1][0]
		return 'multipart/form-data', (file_info['filename'], file_info['body'])
	elif 'application/json' in content_type:
		return decode_json(body, strict=True)
	else:
		# Just try to decode json
		return decode_json(body, strict=False, content_type=content_type)

### EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF
