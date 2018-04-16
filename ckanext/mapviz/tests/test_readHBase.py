from nose.tools import assert_true, assert_false, assert_equal, assert_raises

import happybase

conn = None
test_host = "138.68.183.248"
test_namespace = "test"
test_table_name = "osm"
test_filename = "testfile.osm"
encoding = 'utf-8'

def _encode_dict(data, encoding = 'utf-8'):
	return {k.encode(encoding):v.encode(encoding) for k,v in data.items()}

import json
import xmltodict
from deepdiff import DeepDiff 	

def _xml_equal(a, b):
	"""
	Compares two XML documents (as string or etree)

	Does not care about element order
	"""
	ddiff = DeepDiff(json.loads(json.dumps((xmltodict.parse(a)))),json.loads(json.dumps((xmltodict.parse(b)))), ignore_order=True)
	return not ddiff

class TestReadHBase(object):
	@classmethod
	def setup_class(cls):
		#Create Test Table
		conn = happybase.Connection(host = test_host, table_prefix = test_namespace, table_prefix_separator = ":")
		conn.open()
		table_fams = {
			'node': dict(),
			'way': dict(),
			'relation': dict(),
			'tag': dict()
		}
		conn.create_table(test_table_name,table_fams)


	def teardown(self):
		#Clear Test Table
		batch_size = 100
		table = conn.table(test_table_name)
		batch = table.batch(batch_size = batch_size)
		for row_key, _ in table.scan():
			batch.delete(row_key.encode(encoding))
		batch.send()
		
	@classmethod
	def teardown_class(cls):
		#Delete Test Table
		conn.delete_table(test_table_name)
		conn.close()

	def test_readOSM_node(self):
		table = conn.table(test_table_name)
		row_id = test_filename + '_node_' + '0'
		row_data = {
			"node:action" : "create",
			"node:lat" : "51.513103",
			"node:lon" : "-0.131213",
			"node:visible" : "true",
			"tag:cycle" : "496",
			"tag:id" : "None",
			"tag:station name" : "Frith Street, Soho"
		}
		table.put(row_id.encode(encoding), _encode_dict(row_data))

		expectedOSM = "<osm><node id=\"0\" action=\"create\" lat=\"51.513103\" lon=\"-0.131213\"  visible=\"true\"><tag k=\"station name\" v=\"Frith Street, Soho\" /><tag k=\"cycle\" v=\"496\" /><tag k=\"id\" v=\"None\" /></node></osm>"

		actualOSM = readOSM(test_host,test_namespace,test_table_name,test_filename)

		assert_true(_xml_equal(expectedOSM,actualOSM))


