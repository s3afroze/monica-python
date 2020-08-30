"""
@author: Shahzeb Afroze

Offical Documentation: https://www.monicahq.com/api/conversations

Description: We will put all conversation related requests here

Todo: 
 - Need to add an efficient try except rule in all functions to make sure string is accepted for example
 - Need to add something to read the respone number and tell if there is a problem and if the post request was successful
 	instead of sending json dict

"""

import time
import pandas as pd
import requests
import json
from monica.utils import Utils

basic_api = 'https://app.monicahq.com/api'


class Contact_Field_Types:
	def __init__(self, access_token, wait_time=1):
		"""
		Connect with monica Contact_Field_Types API found at https://www.monicahq.com/api/conversations

		Parameters: 
		-----------
			access_token: str
				token retreived from monica platform

			wait_time: int
				seconds to wait after every request sent

		"""
		headers = {'Authorization': f'Bearer {access_token}', 
					'Content-type': 'application/json', 
					'Accept': 'text/plain'}
		
		self.headers = headers	
		self.basic_api = basic_api
		self.wait_time = wait_time
		self.utils = Utils()

	def list_all(self):
		"""
		Checkout monica API documentation for detailed description.

		Parameters: None
		-----------

		
		Returns: 
		-------
		json_data: dict/json
			can be easily converted to pandas dataframe	

		"""
		headers = self.headers
		wait_time = self.wait_time
		basic_api = self.basic_api		

		api = f"{basic_api}/contactfieldtypes"

		response = requests.get(api, headers=headers)    

		json_data = response.json()

		return json_data

	def get_contact_field_type_id(self, object_name):
		json_data = self.list_all()
		df = pd.DataFrame(json_data['data'])
		contact_field_type_id = df[df['name']==object_name]['id'].values[0]

		return contact_field_type_id




	