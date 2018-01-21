import ckan.plugins as p
import ckan.plugins.toolkit as toolkit


class MapvizPlugin(p.SingletonPlugin):
	p.implements(p.IConfigurer)
	p.implements(p.IResourceView, inherit=True)
	# p.implements(p.ITemplateHelpers, inherit=True)

	# IConfigurer

	def update_config(self, config_):
		toolkit.add_template_directory(config_, 'templates')
		toolkit.add_public_directory(config_, 'public')
		toolkit.add_resource('fanstatic', 'mapviz')

	# IResourceView
	def info(self):
			return {'name': 'mapviz',# Name of plugin
					'title': p.toolkit._('Mapviz'),# Title to be displayed in interface
					'icon': 'globe',# Icon used.
					'iframed': True}

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
	