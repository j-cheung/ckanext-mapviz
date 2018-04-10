import ckan.plugins as p
import ckan.plugins.toolkit as toolkit

from logging import getLogger

from ckan.common import config

from readHBase import readOSM

log = getLogger(__name__)

class MapvizPlugin(p.SingletonPlugin):
	p.implements(p.IConfigurer)
	p.implements(p.IResourceView, inherit=True)
	# p.implements(p.ITemplateHelpers, inherit=True)

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

	# IResourceView
	def info(self):
			return {'name': 'mapviz',# Name of plugin
					'title': p.toolkit._('Mapviz'),# Title to be displayed in interface
					'icon': 'globe',# Icon used.
					'iframed': True}

	def can_view(self, data_dict): 
		'''defines what types of files can use this view'''
		format_lower = data_dict['resource'].get('format', '').lower()
		correct_format = format_lower in ['geojson','osm']
		return correct_format

	def view_template(self, context, data_dict):
		return 'base.html'

	def setup_template_variables(self, context, data_dict):
		format_lower = data_dict['resource'].get('format', '').lower()
		log.info('Data format {0}'.format(format_lower))
		import ckanext.resourceproxy.plugin as proxy
		self.same_domain = data_dict['resource'].get('on_same_domain')
		if self.proxy_enabled and not self.same_domain:
			data_dict['resource']['original_url'] = \
				data_dict['resource'].get('url')
			proxy_resource_url = proxy.get_proxified_resource_url(data_dict)
			print(proxy_resource_url)
			log.info('Proxy URL {0}'.format(proxy_resource_url))
		hbase_osm = None
		if data_dict['hbase_filename']:
			host = "138.68.183.248"
			hbase_osm = readHBase(host, data_dict['hbase_namespace'], data_dict['hbase_table'], data_dict['hbase_filename'])
		return {'proxy_resource_url':proxy_resource_url,
				'resource_format':format_lower,
				'hbase_osm':hbase_osm}


	# # ITemplateHelpers

	# # Tell CKAN what custom template helper functions this plugin provides,
	# # see the ITemplateHelpers plugin interface.
	# def get_helpers(self):
	# 	return {'helper': helper}
	