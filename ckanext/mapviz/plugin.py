import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class MapvizPlugin(plugins.SingletonPlugin):
	plugins.implements(plugins.IConfigurer)
	plugins.implements(plugins.IResourceView, inherit=True)
	# plugins.implements(plugins.ITemplateHelpers, inherit=True)

	# IConfigurer

	def update_config(self, config_):
		toolkit.add_template_directory(config_, 'templates')
		toolkit.add_public_directory(config_, 'public')
		toolkit.add_resource('fanstatic', 'mapviz')

	# IResourceView
	def info(self):
			return {'name': 'mapviz-view',# Name of plugin
					'title': 'Geovisualization',# Title to be displayed in interface
					'icon': 'globe',# Icon used.
					'iframed': False}

	def can_view(self, data_dict): 
		'''defines what types of files can use this view'''
		return True

	def view_template(self, context, data_dict):
		return 'base.html'

	# # ITemplateHelpers

	# # Tell CKAN what custom template helper functions this plugin provides,
	# # see the ITemplateHelpers plugin interface.
	# def get_helpers(self):
	# 	return {'helper': helper}
	