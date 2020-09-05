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
		
		linkedin_messages_file_path = self.linkedin_messages_file_path
		monica_contacts_file_path = self.monica_contacts_file_path
				
		monica_contacts_df = pd.read_csv(monica_contacts_file_path)
		linkedin_df_raw = pd.read_csv(linkedin_messages_file_path)

		# linkedin_df_cleaned = self.apply(linkedin_df_raw).copy() # fixing copy error pandas
		linkedin_df_cleaned = self.apply(linkedin_df_raw)					
		merged_df = self.combine_monica_contacts_with_gmail_df(monica_contacts_df, linkedin_df_cleaned, your_email)

		merged_df['written_by_me'] = False
		merged_df.loc[merged_df['from_dict_email']==your_email, 'written_by_me'] = True

		merged_df['contact_id'] = merged_df.apply(lambda x: max(str(x['contact_id_from']), str(x['contact_id_to'])), axis=1)

		# key identifier
		merged_df['key'] = merged_df['subject'] + merged_df['contact_id']
		

		return merged_df


	def apply(self, df):
		

		df['FROM'] = df['FROM'].str.lower()
		df['TO'] = df['TO'].str.lower()

		df['FROM'] = df['FROM'].str.strip()
		df['TO'] = df['TO'].str.strip()

		df["DATE_TIME"] = pd.to_datetime(df['DATE'])

		df['DATE'] = df['DATE_TIME'].apply(lambda x: x.strftime('%Y-%m-%d'))
		df["CONTENT"] = df["CONTENT"].str.replace("&nbsp", " ")
		# df["CONTENT"] = df["CONTENT"].apply(lambda x: self.deEmojify(x))


		# remove columns not needed for upload
		df.drop(columns=['CONVERSATION TITLE', 'FOLDER', 'SUBJECT'], inplace=True)

		return df


	def combine_monica_contacts_with_linkedin_df(self, monica_contacts_df, linkedin_df_cleaned, your_email):
		utils = self.utils
		contact_id_dict = utils.create_contact_id_dict(monica_contacts_df)
		linkedin_df_cleaned = linkedin_df_cleaned.copy()	

		linkedin_df_cleaned['contact_id_from'] = linkedin_df_cleaned['from_dict_name'].apply(lambda x:utils.retreive_contact_id(full_name=x, contact_id_dict=contact_id_dict))
		linkedin_df_cleaned['contact_id_to'] = linkedin_df_cleaned['to_dict_name'].apply(lambda x:utils.retreive_contact_id(full_name=x, contact_id_dict=contact_id_dict))
		
		linkedin_df_cleaned.loc[linkedin_df_cleaned['from_dict_email']==your_email, 'contact_id_from'] = ""
		linkedin_df_cleaned.loc[linkedin_df_cleaned['to_dict_email']==your_email, 'contact_id_to'] = ""

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

