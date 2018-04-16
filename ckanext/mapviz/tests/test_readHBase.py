from nose.tools import assert_true, assert_false, assert_equal, assert_raises
import happybase
import json
import xmltodict
from deepdiff import DeepDiff 	
import ckanext.mapviz.utils.readHBase as readHBase

conn = None
test_host = "138.68.183.248"
test_namespace = "mapviz_test"
test_table_name = "osm"
test_filename = "testfile.osm"
encoding = 'utf-8'

def _encode_dict(data, encoding = 'utf-8'):
	return {k.encode(encoding):v.encode(encoding) for k,v in data.items()}


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
		cls.conn = happybase.Connection(host = test_host, table_prefix = test_namespace, table_prefix_separator = ":")
		cls.conn.open()
		table_fams = {
			'node': dict(),
			'way': dict(),
			'relation': dict(),
			'tag': dict()
		}
		if test_table_name in cls.conn.tables():
			cls.conn.disable_table(test_table_name)
			cls.conn.delete_table(test_table_name)
		cls.conn.create_table(test_table_name,table_fams)


	def teardown(self):
		#Clear Test Table
		batch_size = 100
		table = self.conn.table(test_table_name)
		# batch = table.batch(batch_size = batch_size)
		for row_key, _ in table.scan():
			table.delete(row_key.encode(encoding))
		# batch.send()
		
	@classmethod
	def teardown_class(cls):
		#Delete Test Table
		if test_table_name in cls.conn.tables():
			cls.conn.disable_table(test_table_name)
			cls.conn.delete_table(test_table_name)
		cls.conn.close()

	def test_readOSM_node(self):
		table = self.conn.table(test_table_name)
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
		actualOSM = readHBase.readOSM(test_host,test_namespace,test_table_name,test_filename)
		assert_true(_xml_equal(expectedOSM,actualOSM))

	def test_readOSM_way(self):
		table = self.conn.table(test_table_name)
		row_id = test_filename + '_way_' + '38407529'
		row_data = {
			"way:timestamp" : "2009-08-02T03:37:41Z",
			"way:user" : "Apo42",
			"way:visible" : "true",
			"way:version" : "1",
			"way:nd_ref_0" : "453966480",
			"way:nd_ref_1" : "453966490",
			"way:nd_ref_2" : "453966482",
			"way:nd_ref_3" : "453966130",
			"way:nd_ref_4" : "453966143",
			"way:nd_ref_5" : "453966480",
			"tag:park:type" : "state_park",
			"tag:csp:unitcode" : "537",
			"tag:admin_level" : "4",
			"tag:name" : "Malibu Creek State Park",
			"tag:csp:globalid" : "{4A422954-089E-407F-A5B3-1E808F830EAA}",
			"tag:leisure" : "park",
			"tag:attribution" : "CASIL CSP_Opbdys072008",
			"tag:note" : "simplified with josm to reduce node #",
			"tag:boundary" : "national_park"
		}
		table.put(row_id.encode(encoding), _encode_dict(row_data))

		expectedOSM = "<osm><way id=\"38407529\" timestamp=\"2009-08-02T03:37:41Z\" user=\"Apo42\" visible=\"true\" version=\"1\"><nd ref=\"453966480\" /><nd ref=\"453966490\" /><nd ref=\"453966482\" /><nd ref=\"453966130\" /><nd ref=\"453966143\" /><nd ref=\"453966480\" /><tag k=\"park:type\" v=\"state_park\" /><tag k=\"csp:unitcode\" v=\"537\" /><tag k=\"admin_level\" v=\"4\" /><tag k=\"name\" v=\"Malibu Creek State Park\" /><tag k=\"csp:globalid\" v=\"{4A422954-089E-407F-A5B3-1E808F830EAA}\" /><tag k=\"leisure\" v=\"park\" /><tag k=\"attribution\" v=\"CASIL CSP_Opbdys072008\" /><tag k=\"note\" v=\"simplified with josm to reduce node #\" /><tag k=\"boundary\" v=\"national_park\" /></way></osm>"
		actualOSM = readHBase.readOSM(test_host,test_namespace,test_table_name,test_filename)
		assert_true(_xml_equal(expectedOSM,actualOSM))

	def test_readOSM_relation(self):
		table = self.conn.table(test_table_name)
		row_id = test_filename + '_way_' + '11'
		row_data = {
			"relation:visible" : "true",
			"relation:version" : "39",
			"relation:changeset" : "44849789",
			"relation:timestamp" : "2017-01-02T16:53:31Z",
			"relation:user" : "fx99",
			"relation:uid" : "130472",
			"relation:mem_type_0" : "way",
			"relation:mem_ref_0" : "8125151",
			"relation:mem_role_0" : "outer",
			"relation:mem_type_1" : "way",
			"relation:mem_ref_1" : "249285853",
			"relation:mem_role_1" : "inner",
			"relation:mem_type_2" : "way",
			"relation:mem_ref_2" : "249285856",
			"relation:mem_role_2" : "inner",
			"tag:name" : "Tween Pond",
			"tag:natural" : "water",
			"tag:type" : "multipolygon"
		}
		table.put(row_id.encode(encoding), _encode_dict(row_data))

		expectedOSM = "<osm><relation id=\"11\" visible=\"true\" version=\"39\" changeset=\"44849789\" timestamp=\"2017-01-02T16:53:31Z\" user=\"fx99\" uid=\"130472\"><member type=\"way\" ref=\"8125151\" role=\"outer\"/><member type=\"way\" ref=\"249285853\" role=\"inner\"/><member type=\"way\" ref=\"249285856\" role=\"inner\"/><tag k=\"name\" v=\"Tween Pond\"/><tag k=\"natural\" v=\"water\"/><tag k=\"type\" v=\"multipolygon\"/></relation></osm>"
		actualOSM = readHBase.readOSM(test_host,test_namespace,test_table_name,test_filename)
		print(actualOSM)
		assert_true(_xml_equal(expectedOSM,actualOSM))

