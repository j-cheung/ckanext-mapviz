# encoding: utf-8

'''Tests for the ckanext.mapviz extension.

'''

from nose.tools import assert_true, assert_false, assert_equal, assert_raises

import ckan.model as model
import ckan.plugins
from ckan.plugins.toolkit import NotAuthorized, ObjectNotFound
import ckan.tests.factories as factories
import ckan.logic as logic

import ckan.tests.helpers as helpers

class TestMapvizPlugin(object):
	@classmethod
	def setup_class(cls):
		ckan.plugins.load('mapviz')
		if not ckan.plugins.plugin_loaded('resource_proxy'):
			ckan.plugins.load('resource_proxy')
		cls.plugin = ckan.plugins.get_plugin('mapviz')
		if not ckan.plugins.plugin_loaded('image_view'):
			ckan.plugins.load('image_view')

	def teardown(self):
		model.repo.rebuild_db()

	@classmethod
	def teardown_class(cls):
		ckan.plugins.unload('mapviz')
		ckan.plugins.unload('image_view')
		ckan.plugins.load('resource_proxy')

	def test_can_view_with_format(self):
		for resource_format in ['geojson', 'osm']:
			data_dict = {'resource':{'url' : 'http://dummy.link.data',
									 'format' : resource_format,
									 'on_same_domain': True}}
			assert_true(self.plugin.can_view(data_dict)) 

	def test_cannot_view_with_format(self):
		for resource_format in ['xml', 'txt']:
			data_dict = {'resource':{'url' : 'http://dummy.link.data',
									 'format' : resource_format,
									 'on_same_domain': True}}
			assert_false(self.plugin.can_view(data_dict))
	
	def test_can_view_from_url(self):
		for resource_format in ['geojson', 'osm']:
			data_dict = {'resource':{'url' : 'http://dummy.link.data/data.'+resource_format,
									 'format' : '',
									 'on_same_domain': True}}
			assert_true(self.plugin.can_view(data_dict)) 


	def test_cannot_view_from_url(self):
		for resource_format in ['xml', 'txt']:
			data_dict = {'resource':{'url' : 'http://dummy.link.data/data.'+resource_format,
									 'format' : '',
									 'on_same_domain': True}}
			assert_false(self.plugin.can_view(data_dict))

	def test_cannot_view_bad_url(self):
		for resource_format in ['geojson','osm','xml', 'txt']:
			data_dict = {'resource':{'url' : 'http://bad.link.data.'+resource_format,
									 'format' : '',
									 'on_same_domain': True}}
			assert_false(self.plugin.can_view(data_dict))

	# @helpers.change_config('ckan.plugins', 'resource_proxy')
	def test_can_view_proxy(self):
		for resource_format in ['geojson', 'osm']:
			data_dict = {'resource':{'url' : 'http://dummy.link.data/data.'+resource_format,
									 'format' : resource_format,
									 'on_same_domain': False}}
			# print(self.plugin.proxy_enabled)
			# self.plugin.proxy_enabled = True
			assert_true(self.plugin.can_view(data_dict)) 

	def test_cannot_view_proxy(self):
		for resource_format in ['geojson', 'osm']:
			data_dict = {'resource':{'url' : 'http://dummy.link.data/data.'+resource_format,
									 'format' : resource_format,
									 'on_same_domain': False}}
			# print(self.plugin.proxy_enabled)
			self.plugin.proxy_enabled = False
			assert_false(self.plugin.can_view(data_dict)) 
	# def test_
