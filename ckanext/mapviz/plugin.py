import ckan.plugins as p
import ckan.plugins.toolkit as toolkit

from logging import getLogger

from ckan.common import config

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

	# IResourceView
	def info(self):
			return {'name': 'mapviz',# Name of plugin
					'title': p.toolkit._('Mapviz'),# Title to be displayed in interface
					'icon': 'globe',# Icon used.
					'iframed': True}

	def can_view(self, data_dict): 
		'''defines what types of files can use this view'''
		format_lower = data_dict['resource'].get('format', '').lower()
		log.debug(format_lower)
		return True

	def view_template(self, context, data_dict):
		return 'base.html'

	def setup_template_variables(self, context, data_dict):
		import ckanext.resourceproxy.plugin as proxy
		self.same_domain = data_dict['resource'].get('on_same_domain')
		if self.proxy_enabled and not self.same_domain:
			data_dict['resource']['original_url'] = \
				data_dict['resource'].get('url')
			# data_dict['resource']['url'] = \
			# 	proxy.get_proxified_resource_url(data_dict)
			proxy_resource_url = proxy.get_proxified_resource_url(data_dict)
		return {'proxy_resource_url':proxy_resource_url}

	# # ITemplateHelpers

	# # Tell CKAN what custom template helper functions this plugin provides,
	# # see the ITemplateHelpers plugin interface.
	# def get_helpers(self):
	# 	return {'helper': helper}
	