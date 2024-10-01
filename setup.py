from setuptools import setup, find_packages

setup(
	name='project0',
	version='1.0',
	author='Sai Prakash Mushkara',
	author_email='s.mushkara@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs', 'resources')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']
)