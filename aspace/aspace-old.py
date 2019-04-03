import requests
import json
class Aspace(object):	
	'''
	Base client object for ArchivesSpace backend
	
	Attributes:
		uname: username 
		pword: password
		api: url of api for particular instance of archivesspace 
		repo: repository in ArchivesSpace. Typically set to 2
		
	INITIALIZING THE CLIENT
		>>>from aspace import Aspace
		>>>client = Aspace('uname', 'pword', 'api', repo number)
		
		
		
		
	RENEWING SESSION
		>>>client.login()
			
	
	'''
	def __init__(self, uname, pword, api, repo):
		self.uname = uname
		self.pword = pword
		self.api = api
		self.repo = repo
		
		response = requests.post(self.api+'/users/'+self.uname+'/login?password='+self.pword)
		status = response.status_code
		if status == 403:
			print('Credentials denied!')

		try:
			json_response = response.json()
			session = json_response['session']
			header = {'X-ArchivesSpace-Session':session}
			self.session = header
		except KeyError:
			print('Login failed!')
			
			
	#Return session token	
	def get_session(self):
		return self.session
		
	#Used for renewing session, will replace active session with previous token
	def login(self):
		query = requests.post(self.api+'/users/'+self.uname+'/login?password='+self.pword).json()
		print(query)
		session = query['session']
		header = {'X-ArchivesSpace-Session':session}
		self.session = header

	#Retrieves JSON for container given the ID	
	def get_container(self, id):
		self.id = id
		query_url = self.api+'/repositories/'+str(self.repo)+'/top_containers/'+str(self.id)
		lookup = requests.get(query_url, headers=self.session).json()
		return lookup
	#Retrieves list of all top container IDs
	def get_container_ids(self):
		query_url = self.api+'/repositories/'+str(self.repo)+'/top_containers?all_ids=true'
		lookup = requests.get(query_url, headers=self.session).json()
		id_list = list(lookup)
		return id_list
	
	#Retrieves JSON for an archival object given the ID	
	def get_archival_object(self, id):
		self.id = id
		query_url = self.api+'/repositories/'+str(self.repo)+'/archival_objects/'+str(self.id)
		lookup = requests.get(query_url, headers=self.session).json()
		return lookup
		

	'''
	FUNCTIONS FOR RECORDS OF ANY TYPE
		get_field: takes record (any type) and field name in quotes (e.g. 'title') --> returns value of field
		update_record: takes record, field to be updated, and new value --> returns updated record (NOTE: Changes are not reflected on server. Use dedicated function for record type to send changes to server). 
			This function does not recognize controlled value fields. Violations of controlled value rules will only 
			be registered when you try to send those changes to the server. 
		get_id: takes record --> returns ID of that record (NOTE: Use record['uri'] to get full uri instead of just number) 
	'''
	
	def get_id(self, record):
		uri = record['uri']
		id = uri.split('/')[-1]
		return id
	
	def get_field(self, record, field):
		self.field = field
		self.record = record
		try:
			value = record[field]
			return value
		except KeyError:
			print('Field not found in record!')
			
	def last_modified(self, record):
		self.record = record
		try:
			last_modified = record['last_modified_by']
			return last_modified
		except KeyError:
			print('No record of last modification')
			
	def change_record(self, record, field, new_value):
		self.field = field
		try: 
			record[field] = new_value
			new = json.dumps(record)
			return new
		except KeyError:
			print('Field not found!')

	def update_container(self, record, id):
		query_url = self.api+'/repositories/'+str(self.repo)+'/top_containers/'+str(self.id)
		update_sent = requests.post(query_url, headers=self.session, data=record).json()
		#print(update_sent)
		try:
			status = update_sent['status']
			if status == 'Updated':
				print('Update successful!')
			else: 
				print('Update failed!')
		except KeyError:
			status = update_sent['error']
			print(status)
			return record
	
	'''
	FUNCTIONS FOR WORKING WITH RESOURCES:
		get_extents: takes resource record --> returns all extents for that resource
		get_instances: takes resource record --> returns all instances for that resource
		get_resource_tc: takes resource record --> returns record for container record for that resource
		update_resource: takes resource record and id --> updates record on ArchviesSpace
		
		To GET a resource:
		>>>resource = client.get_resource(id)
		

	'''	
	
	
	#Retrieves JSON for a resource given the ID	
	def get_resource(self, id):
		self.id = id
		query_url = self.api+'/repositories/'+str(self.repo)+'/resources/'+str(self.id)
		lookup = requests.get(query_url, headers=self.session).json()
		return lookup		
		
		
	#get extents from resource record 		
	def get_extents(self, resource_record):
		extents = resource_record['extents']
		return extents
		
		
	#get instances from resource record -- same method can also be used for archival object records	
	def get_instances(self, resource_record):
		instances = resource_record['instances']
		return instances
			
	#return record for top container of particular resource 
	def get_resource_tc(self, resource_record):
		instances = self.get_instances(resource_record)
		try:
			l = instances[0]
			tc = l['sub_container']['top_container']['ref']
			url_split = tc.split('/')
			tc_uri = url_split[-1]
			container = self.get_container(tc_uri)
			return container
		except IndexError:
			print('No containers in instances')
			res_id = self.get_id(resource_record)
			return res_id

	def get_resource_ids(self):
		query_url = self.api+'/repositories/'+str(self.repo)+'/resources?all_ids=true'
		lookup = requests.get(query_url, headers=self.session).json()
		id_list = list(lookup)
		return id_list
		
		#works now 	(needs more testing) 	
	def update_resource(self, record, id):
		#new_record = json.dumps(record)
		query_url = self.api+'/repositories/'+str(self.repo)+'/resources/'+str(self.id)
		update_sent = requests.post(query_url, headers=self.session, data=record).json()
		#print(update_sent)
		try:
			status = update_sent['status']
			if status == 'Updated':
				print('Update successful!')
			else: 
				print('Update failed!')
		except KeyError:
			status = update_sent['error']
			print(status)
			return record
	

	'''
	WRITING FINDING AIDS/RECORDS TO FILE
		These utilize built in functions to generate finding aids and MARC records from resource in ArchivesSpace, so there isn't a way to change the EAD unless you change the resulting file
		write_ead: takes id and file name and writes an EAD file in XML format
		write_ead_pdf: takes id and file name and writes an EAD in PDF format  
		write_ead3: takes id and file name and writes an EAD3 file in XML format
		write_ead3_pdf: takes id and file name and writes an EAD3 in PDF format  
		write_marc: takes id and file name and writes a MARCXML file 
		
	
	'''

	
	def write_ead(self, id, fname):
		fname = fname + '.xml'
		xml_url = self.api+'/repositories/'+str(self.repo)+'/resource_descriptions/'+str(id)+'.xml'
		r = requests.get(xml_url, headers=self.session)
		xml_str = r.content.decode('utf-8')
		with open(fname, 'w') as f:
			f.write(xml_str)
	
	def write_ead_pdf(self, id, fname):
		fname = fname + '.pdf'
		xml_url = self.api+'/repositories/'+str(self.repo)+'/resource_descriptions/'+str(id)+'.pdf'
		r = requests.get(xml_url, headers=self.session)
		#r_str = r.content.decode('utf-8')
		with open(fname, 'wb') as f:
			f.write(r.content)
			
	def write_ead3_pdf(self, id, fname):
		fname = fname + '.pdf'
		xml_url = self.api+'/repositories/'+str(self.repo)+'/resource_descriptions/'+str(id)+'.pdf?ead3=true'
		r = requests.get(xml_url, headers=self.session)
		#r_str = r.content.decode('utf-8')
		with open(fname, 'wb') as f:
			f.write(r.content)		
			
	def write_ead3(self, id, fname):
		fname = fname + '.xml'
		xml_url = self.api+'/repositories/'+str(self.repo)+'/resource_descriptions/'+str(id)+'.xml?ead3=true'
		r = requests.get(xml_url, headers=self.session)
		xml_str = r.content.decode('utf-8')
		with open(fname, 'w') as f:
			f.write(xml_str)
			
	def write_marc(self, id, fname):
		fname = fname + '.xml'
		xml_url = self.api+'/repositories/'+str(self.repo)+'/resources/marc21/'+str(id)+'.xml'
		r = requests.get(xml_url, headers=self.session)
		xml_str = r.content.decode('utf-8')
		with open(fname, 'w') as f:
			f.write(xml_str)
	

	'''
	FUNCTIONS FOR WORKING WITH ARCHIVAL OBJECTS
		get_ancestors: takes archival object record --> returns list of ancestors for that object
			ex: >>>client.get_ancestors(record) --> [{'ref': '/repositories/2/archival_objects/3', 'level': 'file'}, {'ref': '/repositories/2/resources/10', 'level': 'collection'}]
		update_object: takes archival object record & id --> updates record on server and returns success (or error) message
	'''
	def get_ancestors(self, record):
		ancestors = record['ancestors']
		return ancestors
		
	
	def update_object(self, record, id):
		query_url = self.api+'/repositories/'+str(self.repo)+'/archival_objects/'+str(self.id)
		update_sent = requests.post(query_url, headers=self.session, data=record).json()
		try:
			status = update_sent['status']
			if status == 'Updated':
				print('Update successful!')
			else: 
				print('Update failed!')
		except KeyError:
			status = update_sent['error']
			print(status)
			return record
	
	'''
	SEARCHING VIA API
		field_search: takes a search term and a field and returns search results for that term&field combo in a flat list
			NOTE: this function does not test whether the field exists, but will throw a KeyError when interpreting results if the field doesn't exist
		keyword_search: takes a search term and returns results for that keyword search in a flat list
	

		requests_test 
	WORKING WITH SEARCH RESULTS
		analyze_results: takes a flat list resulting from one of the above searches and returns:
			a list of tuples summarizing the different record types returned and their counts &
			a dictionary of the records organized by record type 
		

	'''
	
	def field_search(self, search_term, field):
		r, url = self._search(search_term, field)
		hits, pages, page_size = self.results_info(r)
		urls = self.get_search_urls(hits, page_size, url)
		if len(urls) > 100:
			proceed = input('This search returned more than 100 pages of records, which can take a while to collect. Do you want to proceed? y/n\n')
			if 'y' in proceed:
				records = self.get_all_records(urls)
				flat_records = [y for x in records for y in x]
				return flat_records
		if len(urls) <= 100:
			records = self.get_all_records(urls)
			flat_records = [y for x in records for y in x]
			return flat_records
	
	
	def keyword_search(self, search_term):
		r, url = self._search(search_term, 'keyword')
		hits, pages, page_size = self.results_info(r)
		urls = self.get_search_urls(hits, page_size, url)
		if len(urls) > 100:
			proceed = input('This search returned more than 100 pages of records, which can take a while to collect. Do you want to proceed? y/n\n')
			if 'y' in proceed:
				records = self.get_all_records(urls)
				flat_records = [y for x in records for y in x]
				return flat_records
		if len(urls) <= 100:
			records = self.get_all_records(urls)
			flat_records = [y for x in records for y in x]
			return flat_records
	
	def analyze_results(self, records):
		results = []
		type_dict = {}
		for i in records:
			uri = i['uri']
			type = uri.split('/')[-2]
			if type not in type_dict:
				type_dict[type] = [i]
			if type in type_dict:
				type_dict[type].append(i)
		for k, v in type_dict.items():
			l = len(v)
			t = (k, l)
			results.append(t)		
		print(results)		
		return type_dict
	
	def _search(self, search_term, field):
		wrapper = {}
		query = {}
		query['field'] = field
		query['value'] = search_term
		query['jsonmodel_type'] = 'field_query'
		query['negated'] = False
		query['literal'] = False
		query_json = json.dumps(query)
		s = '{\"query\":'+query_json+'}'
		search_url = self.api+'/search?page=1&aq='+s
		r = requests.get(search_url, headers=self.session).json()
		return r, search_url 
	
	def get_search_urls(self, hits, page_size, search_url):
		urls = [] 
		n = int(hits / page_size)
		r = hits % page_size 
		p = n
		pgs = list(range(1, p))
		if r > 0:
			p = n+2
			pgs = list(range(1, p))
		
		for i in pgs:
			tmp = '=' + str(i)
			new = search_url.replace('=1', tmp)
			urls.append(new)	
		return urls
	
	def results_info(self, r):
		records = []
		all_results = [] 
		hits = r['total_hits']
		print('Total results: ' + str(hits))
		pages = r['last_page']
		print('Total pages: ' + str(pages))
		page_size = r['page_size']
		return hits, pages, page_size
		
	def get_all_records(self, urls):
		records = []
		for url in urls:
			r = requests.get(url, headers=self.session).json()
			res = r['results']
			records.append(res)
		return records		
	'''
	FUNCTIONS FOR WORKING WITH CONTROLLED VALUES
	
	'''

	def get_enumeration(self, id):
		self.id = str(id)
		url = self.api+'/config/enumerations/'+self.id
		r = requests.get(url, headers=self.session).json()
		return r
	
