"""
Copyright 2017 Deepgram
"""

import inspect
from contextlib import contextmanager
from collections import defaultdict
from functools import wraps
import logging

logger = logging.getLogger(__name__)

_aspects = defaultdict(list)					# pylint: disable=invalid-name
UNDEFINED = object()

###############################################################################
def push_aspect(name, func):
	""" Adds a new aspect to the aspect stack.
	"""
	_aspects[name].append(func)
	return func

###############################################################################
def pop_aspect(name):
	""" Removes an aspect from the aspect stack.
	"""
	_aspects[name].pop()

###############################################################################
def has_self(func):
	""" Returns True if the function takes 'self' as an argument.
	"""
	return 'self' in inspect.signature(func).parameters

###############################################################################
def aspect(name):
	""" Injects an aspect into a function.
	"""
	###########################################################################
	def decorator(func):
		""" Injects an aspect.
		"""
		#######################################################################
		@wraps(func)
		def wrapper(*args, **kwargs):
			""" Apply the aspect.
			"""
			try:
				aspect_func = _aspects[name][-1]
			except IndexError:
				raise ValueError('No such aspect defined: {}'.format(name))
			if has_self(aspect_func):
				if not has_self(func):
					raise ValueError('Aspect requires "self": {}'.format(name))
				value = aspect_func(args[0])
			else:
				value = aspect_func()
			kwargs[name] = value
			return func(*args, **kwargs)
		return wrapper
	return decorator

###############################################################################
def _dynamic(name=None):
	""" Defines an aspect that is evaluated every time the decorated function
		is called.
	"""
	if not isinstance(name, (type(None), str)):
		if callable(name):
			raise ValueError('Invalid use of @aspect decorator. It looks like '
				'you may have forgotten that this is a decorator function, so '
				'you need to call the decorator with parentheses, like this: '
				'@aspect.dynamic().')
		raise ValueError('Invalid value for aspect name: {}'.format(name))
	###########################################################################
	def decorator(func):
		""" The aspect registration decorator.
		"""
		return push_aspect(name or func.__name__, func)
	return decorator
aspect.dynamic = _dynamic

###############################################################################
@contextmanager
def _context(name, func):
	""" Context manager for temporarily modifying the behavior of an aspect.
	"""
	push_aspect(name, func)
	yield
	pop_aspect(name)
aspect.context = _context

###############################################################################
def _static(name=None, value_func=UNDEFINED):
	""" Defines an aspect that is lazily evaluated only once, when it is first
		used.
	"""
	if not isinstance(name, (type(None), str)):
		if callable(name):
			raise ValueError('Invalid use of @aspect decorator. It looks like '
				'you may have forgotten that this is a decorator function, so '
				'you need to call the decorator with parentheses, like this: '
				'@aspect.static().')
		raise ValueError('Invalid value for aspect name: {}'.format(name))
	###########################################################################
	def decorator(func):
		""" The aspect registration decorator.
		"""
		if has_self(func):
			###################################################################
			def evaluate(self):
				""" Function wrapper for lazily evaluating the aspect.
				"""
				if not hasattr(evaluate, 'value'):
					evaluate.value = func(self)
				return evaluate.value
		else:
			###################################################################
			def evaluate():
				""" Function wrapper for lazily evaluating the aspect.
				"""
				if not hasattr(evaluate, 'value'):
					evaluate.value = func()
				return evaluate.value
		return push_aspect(name or func.__name__, evaluate)
	if value_func is not UNDEFINED:
		return decorator(value_func)
	return decorator
aspect.static = _static

###############################################################################
def _constant(name, value):
	""" Defines an aspect that is a single value.
	"""
	return push_aspect(name, lambda: value)
aspect.constant = _constant

###############################################################################
# pylint: disable=protected-access
def _instance(name=None):
	""" Defines an aspect that is lazily evaluated only once per class
		instance, when it is first used by that instance.
	"""
	if not isinstance(name, (type(None), str)):
		if callable(name):
			raise ValueError('Invalid use of @aspect decorator. It looks like '
				'you may have forgotten that this is a decorator function, so '
				'you need to call the decorator with parentheses, like this: '
				'@aspect.instance().')
		raise ValueError('Invalid value for aspect name: {}'.format(name))
	###########################################################################
	def decorator(func):
		""" The aspect registration decorator.
		"""
		func_name = name or func.__name__

		#######################################################################
		@wraps(func)
		def modified_func(self):
			""" Function wrapper for lazily evaluating the aspect.
			"""
			if not hasattr(self, '_aspects_values'):
				self._aspects_values = {}
			if func_name not in self._aspects_values:
				value = func(self) if has_self(func) else func()
				self._aspects_values[func_name] = value
			return self._aspects_values[func_name]

		return push_aspect(func_name, modified_func)
	return decorator
# pylint: enable=protected-access

aspect.instance = _instance

### EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF
