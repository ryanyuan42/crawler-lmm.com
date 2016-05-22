from distutils.core import setup
import requests.certs
import py2exe

build_exe_options = {"include_files":[(requests.certs.where(),'cacert.pem')]}

setup(
	name='LY_data_crawler',
	version='1.0',
	description='an app that track data from lmm.com',
	author = 'Tianshu Yuan',
	options={
	'py2exe': {'packages':['requests']},
	'build_exe': build_exe_options
	},
	console = ['crawler.py']
)