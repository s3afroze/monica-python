"""
@author: Shahzeb Afroze

We will put functions to help us clean the data concerning gmail

"""
import re
import pandas as pd
from datetime import datetime
from social.utils import Utils
import jellyfish

class Preprocessing:
	def __init__(self, linkedin_messages_file_path, monica_contacts_file_path):
		"""
		Preparing gmail data for monica conversations

		Parameters: 
		-----------		

		"""
		self.linkedin_messages_file_path = linkedin_messages_file_path
		self.monica_contacts_file_path = monica_contacts_file_path
		self.utils = Utils()


	def prepare_dataframe(self):
		utils = self.utils
		linkedin_messages_file_path = self.linkedin_messages_file_path
		monica_contacts_file_path = self.monica_contacts_file_path
				
		monica_contacts_df = pd.read_csv(monica_contacts_file_path)
		monica_contacts_df['complete_name'] = monica_contacts_df['complete_name'].str.lower()

		linkedin_df_raw = pd.read_csv(linkedin_messages_file_path)

		# linkedin_df_cleaned = self.apply(linkedin_df_raw).copy() # fixing copy error pandas
		linkedin_df_cleaned = self.apply(linkedin_df_raw)			
		my_name = utils.find_my_info(col1='FROM', col2='TO', df=linkedin_df_cleaned)

		merged_df = self.combine_monica_contacts_with_linkedin_df(monica_contacts_df, linkedin_df_cleaned, my_name)

		merged_df['written_by_me'] = False
		merged_df.loc[merged_df['FROM']==my_name, 'written_by_me'] = True

		merged_df['contact_id'] = merged_df.apply(lambda x: max(str(x['contact_id_from']), str(x['contact_id_to'])), axis=1)

		# key identifier
		merged_df['key'] = merged_df['CONVERSATION ID']
		

		return merged_df


	def apply(self, df):
		
		df = df[~df['FROM'].isna()]
		df = df[~df['TO'].isna()]

		df['FROM'] = df['FROM'].str.lower()
		df['TO'] = df['TO'].str.lower()

		df['FROM'] = df['FROM'].str.strip()
		df['TO'] = df['TO'].str.strip()

		df["date_time"] = pd.to_datetime(df['DATE'])

		df['date'] = df['date_time'].apply(lambda x: x.strftime('%Y-%m-%d'))
		df["text"] = df["CONTENT"].str.replace("&nbsp", " ")
		# df["CONTENT"] = df["CONTENT"].apply(lambda x: self.deEmojify(x))


		# remove columns not needed for upload
		df.drop(columns=['CONVERSATION TITLE', 'FOLDER', 'SUBJECT', 'CONTENT', 'DATE'], inplace=True)

		return df

	def prepare_fuzzy_dataframe(self, monica_contacts_df, linkedin_df_cleaned, my_name):
		utils = self.utils
		
		temp_df = pd.DataFrame()
		temp_df['FROM']= linkedin_df_cleaned.drop_duplicates(subset=['FROM'])['FROM']
		temp_df['TO']= linkedin_df_cleaned.drop_duplicates(subset=['TO'])['TO']

		to_list = list(linkedin_df_cleaned.drop_duplicates(subset=['TO'])['TO'].reset_index(drop=True))
		from_list = list(linkedin_df_cleaned.drop_duplicates(subset=['FROM'])['FROM'].reset_index(drop=True))

		all_correspondence = from_list + to_list
		df = pd.DataFrame(all_correspondence, columns=['linkedin_name'])
		df.drop_duplicates(subset='linkedin_name')

		df['linkedin_name'] = df['linkedin_name'].str.lower()
		df = df[~df['linkedin_name'].isna()]

		monica_contact_list = list(monica_contacts_df["complete_name"].str.lower())

		# connect names of monica
		df['monica_name'] = df['linkedin_name'].apply(lambda x:utils.fuzzy_contact_name_match(search_name=x, monica_contact_list=monica_contact_list, my_name=my_name, benchmark=0.8))

		return df


	def combine_monica_contacts_with_linkedin_df(self, monica_contacts_df, linkedin_df_cleaned, my_name):
		utils = self.utils
		fuzzy_df = self.prepare_fuzzy_dataframe(monica_contacts_df, linkedin_df_cleaned, my_name)
		fuzzy_monica_linkedin_dict = utils.create_fuzzy_monica_linkedin_dict(fuzzy_df)
			
		# connect names of monica
		linkedin_df_cleaned['monica_from_full_name'] = linkedin_df_cleaned['FROM'].apply(lambda x:utils.retreive_fuzzy_monica_name(linkedin_name=x, fuzzy_monica_linkedin_dict=fuzzy_monica_linkedin_dict))
		linkedin_df_cleaned['monica_to_full_name'] = linkedin_df_cleaned['TO'].apply(lambda x:utils.retreive_fuzzy_monica_name(linkedin_name=x, fuzzy_monica_linkedin_dict=fuzzy_monica_linkedin_dict))

		contact_id_dict = utils.create_contact_id_dict(monica_contacts_df)
		linkedin_df_cleaned = linkedin_df_cleaned.copy()	

		linkedin_df_cleaned['contact_id_from'] = linkedin_df_cleaned['monica_from_full_name'].apply(lambda x:utils.retreive_contact_id(full_name=x, contact_id_dict=contact_id_dict))
		linkedin_df_cleaned['contact_id_to'] = linkedin_df_cleaned['monica_to_full_name'].apply(lambda x:utils.retreive_contact_id(full_name=x, contact_id_dict=contact_id_dict))

		linkedin_df_cleaned.loc[linkedin_df_cleaned['monica_from_full_name']==my_name, 'contact_id_from'] = ""
		linkedin_df_cleaned.loc[linkedin_df_cleaned['monica_to_full_name']==my_name, 'contact_id_to'] = ""

		return linkedin_df_cleaned


	# credits to @jfs from stackoverflow - https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
	def deEmojify(self, text):
		"""
		Removes emoji from text - sometimes used in subject lines

		Parameters: 
		-----------
		text: str
			text input could be either subject or content of email
		

		Returns: 
		-------
		clean_text: str
			text without emoji

		"""    
		regrex_pattern = re.compile(pattern = "["
									u"\U0001F600-\U0001F64F"  # emoticons
									u"\U0001F300-\U0001F5FF"  # symbols & pictographs
									u"\U0001F680-\U0001F6FF"  # transport & map symbols
									u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
									"]+", flags = re.UNICODE)
		try:
			clean_text = regrex_pattern.sub(r'',text)			
		except:
			clean_text = text

		return clean_text

	def clean_subject_line(self, subject):
		try:
			subject_lower = subject.lower()

			subject_clean = subject_lower.replace('fwd:','')
			subject_clean = subject_clean.replace('re:','')
			subject_clean = subject_clean.replace('fw:','')
			subject_clean = subject_clean.strip()
			
			subject_clean_no_emoji = self.deEmojify(subject_clean)

			return subject_clean_no_emoji

		except:
			return subject

