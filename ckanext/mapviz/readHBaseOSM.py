import happybase

def readHBase():
	host = "138.68.183.248"
	namespace = "sample_data"
	table_name = "osm"
	filename = "corrected.osm"

	conn = happybase.Connection(host = host, table_prefix = namespace, table_prefix_separator = ":")
	conn.open()
	table = conn.table(table_name)
	print(conn.tables())

	encoding = 'utf-8'

	import xml.etree.ElementTree as et
	root = et.Element('osm')

	try:
		for key, data in table.scan(row_prefix=filename.encode(encoding)):
			print(key,data)
			_, node_id = key.decode(encoding).split("-",1)
			print(node_id)
			decoded_dict = {k.decode(encoding):v.decode(encoding) for k, v in data.items()}
			print(decoded_dict)
			node_action = decoded_dict['node:action']
			node_lat = decoded_dict['node:lat']
			node_lon = decoded_dict['node:lon']
			node_visible = decoded_dict['node:visible']
			node = et.Element('node')
			node.set('id',node_id)
			node.set('action',node_action)
			node.set('lat',node_lat)
			node.set('lon',node_lon)
			node.set('visible',node_visible)
			tag_cycle = et.Element('tag')
			tag_cycle.set('k','cycle')
			tag_cycle.set('v',decoded_dict['tag:cycle'])
			node.append(tag_cycle)
			tag_id = et.Element('tag')
			tag_id.set('k','id')
			tag_id.set('v',decoded_dict['tag:id'])
			node.append(tag_id)
			tag_station_name = et.Element('tag')
			tag_station_name.set('k','station name')
			tag_station_name.set('v',decoded_dict['tag:station name'])
			node.append(tag_station_name)
			root.append(node)
	finally:
		conn.close()

	return et.tostring(root)
	# from ElementTree_pretty import prettify
	# print(prettify(root))
