# encoding: utf-8

'''Tests for the ckanext.mapviz extension.

'''

from nose.tools import assert_raises
from nose.tools import assert_equal

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
        cls.plugin = ckan.plugins.get_plugin('mapviz')
        if not ckan.plugins.plugin_loaded('image_view'):
            ckan.plugins.load('image_view')

    def teardown(self):
        model.repo.rebuild_db()

    @classmethod
    def teardown_class(cls):
        ckan.plugins.unload('mapviz')
        ckan.plugins.unload('image_view')

    def test_can_view_with_format(self):
        # dataset = factories.Dataset()
        # resource = factories.Resource(  
        #     package_id=dataset['id'],
        #     url='http://dummy.link.data', 
        #     format='geojson')
        for resource_format in ['geojson', 'osm']:
            data_dict = {'resource':{'url' : 'http://dummy.link.data',
                                     'format' : resource_format}}
            print(resource_format, self.plugin.can_view(data_dict))
            assert self.plugin.can_view(data_dict)

    def test_cannot_view_with_format(self):
        # dataset = factories.Dataset()
        # resource = factories.Resource(  
        #     package_id=dataset['id'],
        #     url='http://dummy.link.data', 
        #     format='xml')
        for resource_format in ['xml', 'txt']:
            data_dict = {'resource':{'url' : 'http://dummy.link.data',
                                     'format' : resource_format}}
            print(resource_format, self.plugin.can_view(data_dict))
            assert not self.p.can_view(data_dict)
    
    def test_can_view_from_url(self):
        for resource_format in ['geojson', 'osm']:
            data_dict = {'resource':{'url' : 'http://dummy.link.data.'+resource_format,
                                     'format' : ''}}
            print(resource_format, self.plugin.can_view(data_dict))
            assert not self.p.can_view(data_dict)


    def test_can_view_from_url(self):
        for resource_format in ['xml', 'txt']:
            data_dict = {'resource':{'url' : 'http://dummy.link.data.'+resource_format,
                                     'format' : ''}}
            print(resource_format, self.plugin.can_view(data_dict))
            assert not self.p.can_view(data_dict)
