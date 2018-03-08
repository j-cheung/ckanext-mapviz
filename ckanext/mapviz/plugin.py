import ckan.plugins as p
import ckan.plugins.toolkit as toolkit

from logging import getLogger

from ckan.common import config

log = getLogger(__name__)

class MapvizPlugin(p.SingletonPlugin, toolkit.DefaultDatasetForm):
	p.implements(p.IConfigurer)
	p.implements(p.IResourceView, inherit=True)
	p.implements(p.IDatasetForm)
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
		log.info('Data format {0}'.format("hi"))
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
			# data_dict['resource']['url'] = \
			# 	proxy.get_proxified_resource_url(data_dict)
			proxy_resource_url = proxy.get_proxified_resource_url(data_dict)
			print(proxy_resource_url)
			log.info('Proxy URL {0}'.format(proxy_resource_url))
		return {'proxy_resource_url':proxy_resource_url,
				'resource_format':format_lower}

	# IDatasetForm

	def _modify_package_schema(self, schema):
		# Add our custom country_code metadata field to the schema.
		schema.update({
				'country_code': [tk.get_validator('ignore_missing'),
					tk.get_converter('convert_to_tags')('country_codes')]
				})
		# Add our custom_test metadata field to the schema, this one will use
		# convert_to_extras instead of convert_to_tags.
		schema.update({
				'custom_text': [tk.get_validator('ignore_missing'),
					tk.get_converter('convert_to_extras')]
				})
		# Add our custom_resource_text metadata field to the schema
		schema['resources'].update({
				'custom_resource_text' : [ tk.get_validator('ignore_missing') ]
				})
		return schema

	def create_package_schema(self):
		schema = super(ExampleIDatasetFormPlugin, self).create_package_schema()
		schema = self._modify_package_schema(schema)
		return schema

	def update_package_schema(self):
		schema = super(ExampleIDatasetFormPlugin, self).update_package_schema()
		schema = self._modify_package_schema(schema)
		return schema

	def show_package_schema(self):
		schema = super(ExampleIDatasetFormPlugin, self).show_package_schema()

		# Don't show vocab tags mixed in with normal 'free' tags
		# (e.g. on dataset pages, or on the search page)
		schema['tags']['__extras'].append(tk.get_converter('free_tags_only'))

		# Add our custom country_code metadata field to the schema.
		schema.update({
			'country_code': [
				tk.get_converter('convert_from_tags')('country_codes'),
				tk.get_validator('ignore_missing')]
			})

		# Add our custom_text field to the dataset schema.
		schema.update({
			'custom_text': [tk.get_converter('convert_from_extras'),
				tk.get_validator('ignore_missing')]
			})

		schema['resources'].update({
				'custom_resource_text' : [ tk.get_validator('ignore_missing') ]
			})
		return schema

	def is_fallback(self):
		# Return True to register this plugin as the default handler for
		# package types not handled by any other IDatasetForm plugin.
		return True

	def package_types(self):
		# This plugin doesn't handle any special package types, it just
		# registers itself as the default (above).
		return []

	# # ITemplateHelpers

	# # Tell CKAN what custom template helper functions this plugin provides,
	# # see the ITemplateHelpers plugin interface.
	# def get_helpers(self):
	# 	return {'helper': helper}
	