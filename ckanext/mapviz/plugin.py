import os
import urlparse

import ckan.plugins as p
import ckan.plugins.toolkit as toolkit

from logging import getLogger

from ckan.common import config

from utils.readHBase import readOSM

log = getLogger(__name__)

class MapvizPlugin(p.SingletonPlugin):
	p.implements(p.IConfigurer)
	p.implements(p.IResourceView, inherit=True)

	# IConfigurer

	def update_config(self, config_):
		toolkit.add_template_directory(config_, 'templates')
		toolkit.add_public_directory(config_, 'public')
		toolkit.add_resource('fanstatic', 'mapviz')
		
		self.proxy_enabled = 'resource_proxy' in config.get('ckan.plugins', '')

	def _guess_format_from_extension(self, url):
		try:
			parsed_url = urlparse.urlparse(url)
			format_lower = (os.path.splitext(parsed_url.path)[1][1:]
							.encode('ascii', 'ignore').lower())
		except ValueError, e:
			log.error('Invalid URL: {0}, {1}'.format(url, e))
			format_lower = ''

		return format_lower		

	def _get_format_lower(self,data_dict):
		format_lower = data_dict['resource'].get('format', '').lower()
		# Guess from file extension
		if not format_lower and data_dict['resource'].get('url'):
			format_lower = self._guess_format_from_extension(
				data_dict['resource'].get('url'))
		return format_lower

	# IResourceView
	def info(self):
			return {'name': 'mapviz',# Name of plugin
					'title': p.toolkit._('Mapviz'),# Title to be displayed in interface
					'icon': 'globe',# Icon used.
					'iframed': True}

	def can_view(self, data_dict): 
		'''defines what types of files can use this view'''
		format_lower = self._get_format_lower(data_dict)
		if not format_lower:
			return False
		correct_format = format_lower in ['geojson','osm']
		same_domain = data_dict['resource'].get('on_same_domain')
		can_view_from_domain = self.proxy_enabled or same_domain
		return correct_format and can_view_from_domain

	def view_template(self, context, data_dict):
		return 'base.html'

	def setup_template_variables(self, context, data_dict):
		resource_format = self._get_format_lower(data_dict)
		import ckanext.resourceproxy.plugin as proxy
		same_domain = data_dict['resource'].get('on_same_domain')
		if self.proxy_enabled and not same_domain:
			resource_url = proxy.get_proxified_resource_url(data_dict)
			log.info('Proxy URL {0}'.format(resource_url))
		else:
			resource_url = data_dict['resource'].get('url')
		hbase_osm = None		
		if data_dict['resource']['hbase_enabled']:
			hbase_host = config.get('ckan.mapviz.hbase_host', '')
			hbase_osm = readOSM(hbase_host, data_dict['resource']['hbase_namespace'], data_dict['resource']['hbase_table'], data_dict['resource']['hbase_filename'])
		return {'resource_url':resource_url,
				'resource_format':resource_format,
				'hbase_osm':hbase_osm}


	# # ITemplateHelpers

	# # Tell CKAN what custom template helper functions this plugin provides,
	# # see the ITemplateHelpers plugin interface.
	# def get_helpers(self):
	# 	return {'helper': helper}
	