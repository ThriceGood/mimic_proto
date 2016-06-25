from flask import render_template
from utils import compare_schema, validate_post_data
import json

class Mimic:

	def get(self, query):
		pass

	def post(self, endpoint, db):
		"""
			so far payload/schema comparison
			is only on dicts where keys are
			in exact order, and NO LISTS!!
		"""
		endpoint = json.loads(endpoint)
		print endpoint
		url = endpoint['url']
		tag = endpoint['tag']
		payload = endpoint['payload']
		try:
		    payload = json.loads(payload)
		except Exception as e:
			return {'error': 'invalid json in payload: {}'.format(e)}
		query = (url, tag)
		response = db.select_endpoint(query=query)
		if type(response) is dict and response.get('error'):
			return {'error': response['error']}
		elif response:
			schema = json.loads(response[0]['schema'])
			result = compare_schema(payload, schema)
			if result:				
				payload_out = response[0]['payload']
				return payload_out
			return {'error': 'bad request schema'}
		return {'error': 'no matching url or tag'}


class Endpoints:

	attrs = ['verb', 'service', 'url', 'tag', 'schema', 'payload']

	def select_endpoint(self):
		pass

	def insert_endpoint(self, post_data, db):
		e = validate_post_data(post_data, Endpoints.attrs)
		if e.get('error'):
			return {'error': e['error']}
		endpoint = (
			e['verb'], e['service'], 
		    e['url'], e['tag'], 
		    e['schema'], e['payload']
		)
		return db.insert_endpoint(endpoint)

	def update_endpoint(self, post_data, db):
		attrs = Endpoints.attrs
		attrs.append('id')
		e = validate_post_data(post_data, attrs)
		attrs.remove('id')
		if e.get('error'):
			return {'error': e['error']}
		endpoint = (
			e['verb'], e['service'], 
		    e['url'], e['tag'], 
		    e['schema'], e['payload'], int(e['id'])
		)
		return db.update_endpoint(endpoint)

	def delete_endpoint(self, id, db):
		return db.delete_endpoint(id)


class UI:

	def docs_page(self):
		return render_template('docs.html')

	def test_page(self):
		return render_template('test.html')

	def index_page(self, db):
		endpoints = db.select_endpoint()
		return render_template('index.html', data=endpoints)

	def insert_endpoint_page(self):
		return render_template('insert.html')

	def update_endpoint_page(self, id, db):
		endpoint = db.select_endpoint(id=id)
		return render_template('update.html', data=endpoint)





















