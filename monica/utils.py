"""
@author: Shahzeb Afroze

Offical Documentation: https://www.monicahq.com/api/

Description: We will put all general functions to help the other classes

"""
import pandas as pd


class Utils:	
	"""
	Helper class for several classes

	"""

	def merge_json_data(self, json_orig, json_new):
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
		json_merged = {}

		all_keys = list(json_orig.keys())

		for key in all_keys:			
			try:
				new_data = json_new[key]
				orignal_data = json_orig[key]
				json_merged[key] = new_data + orignal_data
			except:
				# print(f"{key} will be overwritten with the latest dictionary")
				json_merged[key] = json_new[key] # this will only be "meta" dict for contacts

		return json_merged


		



	