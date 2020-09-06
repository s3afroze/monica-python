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

	def create_fuzzy_monica_linkedin_dict(self, fuzzy_df):

		fuzzy_monica_linkedin_dict = pd.Series(fuzzy_df.linkedin_name.values,index=fuzzy_df.monica_name).to_dict()

		return fuzzy_monica_linkedin_dict
	
	def retreive_fuzzy_monica_name(self, fuzzy_monica_linkedin_dict, linkedin_name):
		try:
			monica_name = fuzzy_monica_linkedin_dict[linkedin_name]
		except:
			monica_name = ''


		return monica_name
	

	def most_frequent(self, List): 
		return max(set(List), key = List.count) 

	# to be used for converting dataframe into columns and applying it to most frequent
	def find_my_info(self, col1, col2, df):
		list_1=list(df[col1].values)
		list_2=list(df[col2].values)

		all_info=list_1 + list_2
		my_info = self.most_frequent(all_info)
		
		return my_info


	def fuzzy_contact_name_match(self, search_name, monica_contact_list, my_name, benchmark=0.85):
		all_score = []
		if search_name!=my_name:
			for monica_contact in monica_contact_list:
				score = jellyfish.jaro_winkler_similarity(search_name, monica_contact)			
				all_score.append(score)
		
			name_matched = self.find_max_score_name(monica_contact_list, all_score, benchmark)
			return name_matched


	def find_max_score_name(self, monica_contact_list, all_score, benchmark):
		max_score = max(all_score)
		if max_score>=benchmark:
			index_of_max_score = all_score.index(max_score)
			name_with_highest_similarity = monica_contact_list[index_of_max_score]
			return name_with_highest_similarity


