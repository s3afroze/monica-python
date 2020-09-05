"""
@author: Shahzeb Afroze

Offical Documentation: https://www.monicahq.com/api/

Description: We will put all general functions to help the other classes

"""
import pandas as pd
from monica.conversations import Conversations
import jellyfish

basic_api = 'https://app.monicahq.com/api'

class Utils:	
	def __init__(self, wait_time=1):
		"""
		Helper class for several classes

		Parameters: 
		-----------
			wait_time: int
				seconds to wait after every request sent

		"""		
		
		self.wait_time = wait_time


	def retreive_contact_id(self, contact_id_dict, full_name):
		"""
		Merges json resonses to create 1 complete json file

		Parameters: 
		-----------
		json_orig: json/dict
			The previous json response from monica

		json_new: json/dict
			The most recent json response from monica
		    		
		Returns: 
		-------
		json_merged: dict/json
			Appending lists within json where ever possible and overwritting the information 
			with the latest json_response where not possible. This will help in the json response
			staying consistent with how the orignal json file looks


		"""
		# we can later apply fuzzy search if later needed
		

		try:
			contact_id = contact_id_dict[full_name]
		except:
			contact_id = ''


		return contact_id
	
	def create_contact_id_dict(self, monica_contacts_df):
		monica_contacts_df.sort_values(by="complete_name", inplace=True)
		monica_contacts_df["complete_name"] = monica_contacts_df["complete_name"].str.lower()
		monica_contacts_df.drop_duplicates(subset=["complete_name"], inplace=True)

		contact_id_dict = pd.Series(monica_contacts_df.id.values,index=monica_contacts_df.complete_name).to_dict()

		return contact_id_dict


	def most_frequent(self, List): 
		return max(set(List), key = List.count) 

	def fuzzy_contact_name_match(search_name, monica_contact_list, benchmark=0.8):
		for monica_contact in monica_contact_list:
			score = jellyfish.jaro_winkler_similarity(search_name, monica_contact)
			if score>=benchmark:
				return 


	# def create_fuzzy_name_email_dict(self, df, name):
	# 	df.drop_duplicates(subset=["from_dict_name"], inplace=True)
	# 	df_subset = df[['from_dict_email', 'from_dict_name']]
	# 	unique_names = df['from_dict_name'].unique()
	# 	fuzzy_scores = process.extract(name, unique_names, scorer=fuzz.token_sort_ratio)
	# 	all_names = [el[0] for el in fuzzy_scores]
	# 	all_scores = [el[1] for el in fuzzy_scores]

	# 	pattern = '|'.join(all_names)

	# 	fuzzy_match_df = df_subset[df_subset['from_dict_name'].str.contains(pattern, case=False)]



	# 	return fuzzy_match_df








