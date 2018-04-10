import happybase

def readOSM(host, namespace, table_name, filename):

	conn = happybase.Connection(host = host, table_prefix = namespace, table_prefix_separator = ":")
	conn.open()
	table = conn.table(table_name)
	print(conn.tables())

	encoding = 'utf-8'

	import xml.etree.ElementTree as et
	root = et.Element('osm')

	try:
		#get nodes
		node_prefix = filename + '_node_'
		for row_key, data in table.scan(row_prefix=node_prefix.encode(encoding)):
			node_id = row_key.decode(encoding).split("_")[-1]
			print(node_id)
			decoded_dict = {k.decode(encoding):v.decode(encoding) for k, v in data.items()}
			print(decoded_dict)
			node = et.Element('node')
			node.set('id',node_id)
			for key, value in decoded_dict.items():
				key_head, key_tail = key.split(':',maxsplit=1)
				if(key_head == "node"):
					node.set(key_tail,value)
				elif(key_head == "tag"):
					tag = et.Element('tag')
					tag.set('k',key_tail)
					tag.set('v',value)
					node.append(tag)
			root.append(node)
		#get ways
		way_prefix = filename + '_way_'
		for row_key, data in table.scan(row_prefix=way_prefix.encode(encoding)):
			way_id = row_key.decode(encoding).split("_")[-1]
			decoded_dict = {k.decode(encoding):v.decode(encoding) for k, v in data.items()}
			way = et.Element('way')
			way.set('id',way_id)
			for key, value in decoded_dict.items():
				key_head, key_tail = key.split(':',maxsplit=1)
				if(key_head == "way"):
					#nodes of way
					if(key_tail[:2] == "nd"):
						way_nd = et.Element('nd')
						way_nd.set('ref',value)
						way.append(way_nd)
					else:
						way.set(key_tail,value)
				elif(key_head == "tag"):
					tag = et.Element('tag')
					tag.set('k',key_tail)
					tag.set('v',value)
					way.append(tag)
			root.append(way)
		#get relations
		relation_prefix = filename + '_relation_'
		for row_key, data in table.scan(row_prefix=relation_prefix.encode(encoding)):
			relation_id = row_key.decode(encoding).split("_")[-1]
			decoded_dict = {k.decode(encoding):v.decode(encoding) for k, v in data.items()}
			relation = et.Element('relation')
			relation.set('id',relation_id)
			for key, value in decoded_dict.items():
				key_head, key_tail = key.split(':',maxsplit=1)
				if(key_head == "relation"):
					#nodes of relation
					if(key_tail[:3] == "mem"):
						if(key_tail[:7] == "mem_ref"):
							relation_mem = et.Element('member')
							relation_mem_id = key_tail[7:]
							relation_mem_type = decoded_dict['relation:mem_type' + relation_mem_id]
							relation_mem_role = decoded_dict['relation:mem_role' + relation_mem_id]
							relation_mem_ref = value
							relation_mem.set('ref',relation_mem_ref)
							relation_mem.set('type',relation_mem_type)
							relation_mem.set('role',relation_mem_role)
							relation.append(relation_mem)
					else:
						relation.set(key_tail,value)
				elif(key_head == "tag"):
					tag = et.Element('tag')
					tag.set('k',key_tail)
					tag.set('v',value)
					relation.append(tag)
			root.append(relation)
	finally:
		conn.close()

	return et.tostring(root)

host = "138.68.183.248"
namespace = "sample_data"
table_name = "osm"
filename = "corrected_amps.osm"
print(readOSM(host, namespace, table_name, filename))
