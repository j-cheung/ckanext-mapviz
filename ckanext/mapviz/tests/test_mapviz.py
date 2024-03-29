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

import mock
import ckanext.mapviz.utils.readHBase

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
		ckan.plugins.unload('resource_proxy')
		model.repo.rebuild_db()

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

	def test_can_view_proxy_enabled(self):
		for resource_format in ['geojson', 'osm']:
			data_dict = {'resource':{'url' : 'http://dummy.link.data/data.'+resource_format,
									 'format' : resource_format,
									 'on_same_domain': False}}
			self.plugin.proxy_enabled = True
			assert_true(self.plugin.can_view(data_dict)) 

	def test_cannot_view_proxy_disabled(self):
		for resource_format in ['geojson', 'osm']:
			data_dict = {'resource':{'url' : 'http://dummy.link.data/data.'+resource_format,
									 'format' : resource_format,
									 'on_same_domain': False}}
			self.plugin.proxy_enabled = False
			assert_false(self.plugin.can_view(data_dict)) 
	
	#Test setup_template_variables

	def test_setup_template_variables_proxy_no_hbase(self):
		self.plugin.proxy_enabled = True
		mock_model = mock.MagicMock()
		context = {'model': mock_model}
		for resource_format in ['geojson', 'osm']:
			resource_url = 'http://dummy.link.data/data.'+resource_format
			import ckanext.resourceproxy.plugin as proxy
			proxy.get_proxified_resource_url = mock.Mock(return_value=resource_url)
			data_dict = {'resource':{'url' : 'http://dummy.link.data/data.'+resource_format,
										 'format' : resource_format,
										 'on_same_domain': False,
										 'hbase_enabled': ''}}
			expected_data = {'resource_url':resource_url,
							 'resource_format':resource_format,
							 'hbase_osm':None}
			result_data = self.plugin.setup_template_variables(context=context,data_dict=data_dict)
			assert_equal(result_data, expected_data)

	def test_setup_template_variables_no_proxy_no_hbase(self):
		self.plugin.proxy_enabled = False
		mock_model = mock.MagicMock()
		context = {'model': mock_model}
		for resource_format in ['geojson', 'osm']:
			resource_url = 'http://dummy.link.data/data.'+resource_format
			data_dict = {'resource':{'url' : 'http://dummy.link.data/data.'+resource_format,
										 'format' : resource_format,
										 'on_same_domain': False,
										 'hbase_enabled': ''}}
			expected_data = {'resource_url':resource_url,
							 'resource_format':resource_format,
							 'hbase_osm':None}
			result_data = self.plugin.setup_template_variables(context=context,data_dict=data_dict)
			assert_equal(result_data, expected_data)

	@mock.patch('ckanext.mapviz.utils.readHBase.readOSM')
	def test_setup_template_variables_proxy_hbase(self, mock_readOSM):
		self.plugin.proxy_enabled = True
		mock_model = mock.MagicMock()
		context = {'model': mock_model}
		for resource_format in ['geojson', 'osm']:
			resource_url = 'http://dummy.link.data/data.'+resource_format
			import ckanext.resourceproxy.plugin as proxy
			proxy.get_proxified_resource_url = mock.Mock(return_value=resource_url)
			data_dict = {'resource':{'url' : 'http://dummy.link.data/data.'+resource_format,
										 'format' : resource_format,
										 'on_same_domain': False,
										 'hbase_enabled': 'True',
										 'hbase_namespace': 'namespace',
										 'hbase_table': 'table',
										 'hbase_filename': 'filename'}}
			mock_osm = "<osm></osm>"
			mock_readOSM.return_value = mock_osm
			expected_data = {'resource_url':resource_url,
							 'resource_format':resource_format,
							 'hbase_osm':mock_osm}
			result_data = self.plugin.setup_template_variables(context=context,data_dict=data_dict)
			assert_equal(result_data, expected_data)
