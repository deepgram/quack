"""
Copyright 2017 Deepgram
"""

###############################################################################
from __future__ import print_function
import sys

PACKAGE = 'quack'

###############################################################################
if sys.version_info < (3, 5):
	print('ERROR: Requires Python 3.5+.', file=sys.stderr)
	sys.exit(1)

###############################################################################
# pylint: disable=wrong-import-position
import os
from setuptools import setup, find_packages
# pylint: enable=wrong-import-position

################################################################################
def readme():
	""" Return the README text.
	"""
	with open('README.rst', 'rb') as fh:
		result = fh.read()

	result = result.decode('utf-8')

	token = '.. package_readme_ends_here'
	mark = result.find(token)
	if mark >= 0:
		result = result[:mark]

	token = '.. package_readme_starts_here'
	mark = result.find(token)
	if mark >= 0:
		result = result[mark+len(token):]

	chunks = []
	skip = False
	for chunk in result.split('\n\n'):
		if not chunk:
			pass
		elif chunk.strip().startswith('.. package_readme_ignore'):
			skip = True
		elif skip:
			skip = False
		else:
			chunks.append(chunk)

	result = '\n\n'.join(chunks)

	return result

################################################################################
def get_version():
	""" Gets the current version of the package.
	"""
	version_py = os.path.join(os.path.dirname(__file__), PACKAGE, 'version.py')
	with open(version_py, 'r') as fh:
		for line in fh:
			if line.startswith('__version__'):
				return line.split('=')[-1].strip() \
					.replace('"', '').replace("'", '')
	raise ValueError('Failed to parse version from: {}'.format(version_py))

################################################################################
setup(
	# Package information
	name=PACKAGE,
	version=get_version(),
	description='Utilities for bootstrapping aspect-oriented HTTP servers',
	long_description=readme(),
	keywords='http server aspect',
	classifiers=[
	],

	# Author information
	url='https://github.com/deepgram/quack',
	author='Adam Sypniewski',
	author_email='adam@deepgram.com',
	license='Proprietary',

	# What is packaged here.
	packages=find_packages(),

	# What to include.
	package_data={
		'': ['*.txt', '*.rst', '*.md']
	},

	# Dependencies
	install_requires=[
		'tornado>=4.5.2'
	],
	dependency_links=[
	],

	# Testing
	test_suite='tests',
	tests_require=[
		'pytest'
	],
	setup_requires=['pytest-runner'],

	#entry_points={
	#	'console_scripts' : ['{pkg}={pkg}.__main__:main'.format(pkg=PACKAGE)]
	#},

	zip_safe=False
)

#### EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF
