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
import requests
import json
from monica.utils import Utils
from pprint import pprint
import pandas as pd

basic_api = 'https://app.monicahq.com/api'


class Conversations:
	def __init__(self, access_token, wait_time=1):
		"""
		Connect with monica conversations API found at https://www.monicahq.com/api/conversations

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

	def list_conversations(self):
		"""
		Gets the conversations from monica. Checkout monica API documentation for detailed description.

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

		api = f"{basic_api}/conversations"

		response = requests.get(api, headers=headers)    
		print(response)

		json_data = response.json()

		return json_data


	def create_conversation_object(self, happened_at, contact_field_type_id, contact_id):
		"""
		Creating a conversation only creates the conversation itself. 
		You will have to add messages one by one to populate it with actual content. 
		Checkout monica API documentation for detailed description.

		Parameters: 
		-----------
		happened_at: str
			The date the conversation happened. Format: YYYY-MM-DD.

		contact_field_type_id: int
			The type of the contact field. Has to be a valid, existing contact field type ID. 			

		contact_id: int
			The ID of the contact that the conversation field is associated with.
		
		Returns: 
		-------
		conversation_id: str
			The ID of created conversation object

		"""
		headers = self.headers
		basic_api = self.basic_api		

		api = f"{basic_api}/conversations"

		payload = {'happened_at': happened_at, 
					'contact_field_type_id': contact_field_type_id,
					'contact_id':contact_id}


		response = requests.post(api,  params=payload, headers=headers)    

		json_data = response.json()

		conversation_id =  json_data['data']['id']

		return conversation_id

	def add_message(self, written_at, written_by_me, content, contact_id, conversation_id):
		"""
		Add a message to a conversation object. Checkout monica API documentation for detailed description.

		Parameters: 
		-----------
		written_at: str
			The date the conversation happened. Format: YYYY-MM-DD.

		written_by_me: Bool
			True if the user has written the message. False if the contact has written the message.

		content: str
			The actual message.
		
		contact_id: int
			The ID of the contact that the conversation is associated with.

		conversation_id: str
			The ID is retreived when conversation_id is created.

		Returns: 
		-------
		json_data: dict/json
			can be easily converted to pandas dataframe	

		"""
		headers = self.headers
		basic_api = self.basic_api		
		contact_id = int(contact_id)

		api = f"{basic_api}/conversations/{conversation_id}/messages"


		payload_raw = {
					"contact_id": contact_id,
					"written_at": written_at,          
					"content": content,
					"written_by_me": written_by_me
					}

		payload = json.dumps(payload_raw) # necessary for converting Boolean to json form e.g True to true

		response = requests.post(api,  json=payload_raw, headers=headers) 
		print(response)
		json_data = response.json()

		return json_data


	def list_conversations_of_a_contact(self, contact_id):
		"""
		List all the conversations of a contact

		"""
		headers = self.headers
		basic_api = self.basic_api		
		contact_id = int(contact_id)

		api = f"{basic_api}/contacts/{contact_id}/conversations"			

		response = requests.get(api, headers=headers) 
		print(response)
		json_data = response.json()

		return json_data

	
	def delete_conversation(self, conversation_id):
		"""
		

		"""
		headers = self.headers
		basic_api = self.basic_api		

		api = f"{basic_api}/conversations/{conversation_id}"

		response = requests.delete(api, headers=headers) 
		print(response)

		# json_data = response.json()
		# return json_data


	def delete_all_conversations_of_a_contact(self, contact_id):
		"""
		List all the conversations of a contact

		"""
		headers = self.headers
		basic_api = self.basic_api	
		wait_time = self.wait_time
			
		all_conversations_json = self.list_conversations_of_a_contact(contact_id)
		try:
			all_conversations_df = pd.DataFrame(all_conversations_json['data'])		
		except:
			print(f"Problem with {contact_id}")

		try:
			all_conversations_id = list(all_conversations_df['id'])
			for conversation_id in all_conversations_id:
				time.sleep(wait_time)
				self.delete_conversation(conversation_id)
		except:			
			# no conversation with this contact
			pass
	# create upload all conversations func

	def add_multiple_messages(self, contact_id, conversation_id, df):
		wait_time = self.wait_time
		time.sleep(wait_time)

		# iterate over messages
		number_of_messages = len(df)

		for i in range(number_of_messages):
			written_by_me = int(df['written_by_me'].values[i]) # 1 & 0 instead of True & False, important because numpy.bool is created from pandas
			written_at = df['date'].values[i]
			content = df['text'].values[i]
			self.add_message(written_at, written_by_me, content, contact_id, conversation_id)




























