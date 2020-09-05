"""
@author: Shahzeb Afroze

Offical Documentation: https://www.monicahq.com/api/contacts

Description: We will put all contacts related requests here

Todo: 
 - Will need to add an efficient try except rule in all functions to make sure string is accepted for example
 - Understand query parameter of get contacts

"""

import time
import requests
from monica.utils import Utils
import json

basic_api = 'https://app.monicahq.com/api'


class Contacts:
	def __init__(self, access_token, wait_time=1):
		"""
		Connect with monica contacts API found at https://www.monicahq.com/api/contacts

		Parameters: 
		-----------
		access_token: str
		token retreived from monica platform

		wait_time: int
		time to wait after every request sent

		"""
		headers = {'Authorization': f'Bearer {access_token}', 'Content-type': 'application/json', 'Accept': 'text/plain'}

		self.headers = headers	
		self.basic_api = basic_api
		self.wait_time = wait_time
		self.utils = Utils()

	def list_contacts(self, limit=10, page=1, sort="updated_at"):
		"""
		Gets the contacts from monica database with page and limit criteria. Checkout monica API documentation for detailed description.

		Parameters: 
		-----------
		limit: int
			Indicates the page size

		page: int
			Indicates the page to return

		sort: str
			Indicates how the query should be ordered by. 
			Possible values: created_at, -created_at, updated_at, -updated_at           
		
		Returns: 
		-------
		json_data: dict/json
			can be easily converted to pandas dataframe	

		"""
		headers = self.headers
		basic_api = self.basic_api		

		api = f"{basic_api}/contacts"

		payload = {'limit': limit, 
					'page': page,
					'sort':sort}


		response = requests.get(api,  params=payload, headers=headers)    
		json_data = response.json()


		return json_data


	def list_all_your_contacts(self, sort="updated_at"):
		"""
		Gets ALL the contacts from monica database. Checkout monica API documentation for detailed description.

		Parameters: 
		-----------
		sort: str
			Indicates how the query should be ordered by. 
			Possible values: created_at, -created_at, updated_at, -updated_at           
		
		Returns: 
		-------
		json_data: dict/json
			can be easily converted to pandas dataframe	

		"""
		utils = self.utils
		wait_time = self.wait_time

		json_orig = self.list_contacts(limit=100, page=1, sort=sort) # pull 1st page
		max_page = json_orig['meta']['last_page']+1
		for page_number in range(2, max_page):
			time.sleep(wait_time)
		    json_new = self.list_contacts(limit=100, page=page_number, sort=sort)
		    json_orig = utils.merge_json_data(json_orig, json_new)

		json_merged = json_orig.copy() # renmaing variable in the end of the loop

		return json_merged


	def create_contact(self, first_name, last_name, gender_id=3, is_birthdate_known=False, is_deceased=False, is_deceased_date_known=False):
		"""
		Create the contacts in monica database. Checkout monica API documentation for detailed description.
		
		"""

		headers = self.headers
		basic_api = self.basic_api		

		api = f"{basic_api}/contacts/"

		payload_raw = {"first_name": first_name,
						"last_name": last_name,
						"gender_id": gender_id,
						"is_birthdate_known": is_birthdate_known,
						"is_deceased": is_deceased,
						"is_deceased_date_known": is_deceased_date_known
						}

		payload = json.dumps(payload_raw) # necessary for converting Boolean to json form e.g True to true
		response = requests.post(api,  params=payload, headers=headers)    
		json_data = response.json()


		return json_data


























