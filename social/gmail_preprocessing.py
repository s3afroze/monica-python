"""
@author: Shahzeb Afroze

We will put functions to help us clean the data concerning gmail

# we can replace email by most popular email in dataframe!!

"""
import re
import pandas as pd
from datetime import datetime
from social.utils import Utils

class Preprocessing:
	def __init__(self, gmail_json_file_path, monica_contacts_file_path):
		"""
		Preparing gmail data for monica conversations

		Parameters: 
		-----------		

		"""
		self.gmail_json_file_path = gmail_json_file_path
		self.monica_contacts_file_path = monica_contacts_file_path
		self.utils = Utils()

	def combine_monica_contacts_with_gmail_df(self, monica_contacts_df, gmail_df_cleaned, my_email):
		utils = self.utils
		contact_id_dict = utils.create_contact_id_dict(monica_contacts_df)
		gmail_df_cleaned = gmail_df_cleaned.copy()	

		gmail_df_cleaned['contact_id_from'] = gmail_df_cleaned['from_dict_name'].apply(lambda x:utils.retreive_contact_id(full_name=x, contact_id_dict=contact_id_dict))
		gmail_df_cleaned['contact_id_to'] = gmail_df_cleaned['to_dict_name'].apply(lambda x:utils.retreive_contact_id(full_name=x, contact_id_dict=contact_id_dict))
		
		gmail_df_cleaned.loc[gmail_df_cleaned['from_dict_email']==my_email, 'contact_id_from'] = ""
		gmail_df_cleaned.loc[gmail_df_cleaned['to_dict_email']==my_email, 'contact_id_to'] = ""

		return gmail_df_cleaned

	def prepare_dataframe(self):
		utils = self.utils
		
		gmail_json_file_path = self.gmail_json_file_path
		monica_contacts_file_path = self.monica_contacts_file_path

		monica_contacts_df = pd.read_csv(monica_contacts_file_path)
		gmail_df_raw = pd.read_json(gmail_json_file_path)

		# gmail_df_cleaned = self.apply(gmail_df_raw).copy() # fixing copy error pandas
		gmail_df_cleaned = self.apply(gmail_df_raw)			
		my_email = utils.find_my_info(col1='to_dict_email', col2='from_dict_email', df=gmail_df_cleaned)
		# print(my_email)

		merged_df = self.combine_monica_contacts_with_gmail_df(monica_contacts_df, gmail_df_cleaned, my_email)

		merged_df['written_by_me'] = False
		merged_df.loc[merged_df['from_dict_email']==my_email, 'written_by_me'] = True

		merged_df['contact_id'] = merged_df.apply(lambda x: max(str(x['contact_id_from']), str(x['contact_id_to'])), axis=1)

		# key identifier
		merged_df['key'] = merged_df['subject'] + merged_df['contact_id']
		

		return merged_df


	def apply(self, df):
		

		df['from_dict'] = df['from'].apply(lambda x: self.extract_first_element(x))
		df['from_dict_email'] = df['from_dict'].apply(lambda x: self.extract_email_address(x))   
		df['from_dict_name'] = df['from_dict'].apply(lambda x: self.extract_name(x)) 

		df['to_dict'] = df['to'].apply(lambda x: self.extract_first_element(x))
		df['to_dict_email'] = df['to_dict'].apply(lambda x: self.extract_email_address(x)) 

		df['to_dict_name'] = df['to_dict'].apply(lambda x: self.extract_name(x)) 

		df['subject'] = df['subject'].apply(lambda x: self.clean_subject_line(x))
		df['date_time'] = df['date']
		df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
		
		# remove addresses with 'no reply'
		df = df[~df['from_dict_email'].str.contains('reply', na=False)]

		# remove columns not needed for upload
		df.drop(columns=['from', 'to', 'from_dict', 'to_dict', 'receivedDate', 
						'html', 'cc', 'headers', 
						'priority', 'attachments', 'bcc', 'alternatives', 
						'references', 'inReplyTo', 'replyTo'], inplace=True)

		return df

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


	def extract_first_element(self, list_of_emails):
		"""
		Extracts the first email from the list

		Parameters: 
		-----------
		list_of_emails: list
			list of emails
		

		Returns: 
		-------
		email: str
			first email in the list for example if the email has been sent to multiple to several people,
			only first email address will be taken into account.

		"""    
		try:
			return list_of_emails[0]
		except:
			return ""

	def extract_name(self, gmail_dict):
		"""
		Extracts the first name from the dict

		Parameters: 
		-----------
		gmail_dict: dict
			dict holding the recipient or sender's information
		

		Returns: 
		-------
		name: str
			name of the recipient or sender of email 

		"""
		try:
			return gmail_dict['name'].lower()
		except:
			return ""


	def extract_email_address(self, gmail_dict):
		"""
		Extracts the email address from the dict

		Parameters: 
		-----------
		gmail_dict: dict
			dict holding the recipient or sender's information
		

		Returns: 
		-------
		email: str
			email of the recipient or sender depending on gmail dict 

		"""
		try:
			return gmail_dict['address'].lower()
		except:
			return ""

	def extract_date(self, date_time):
		"""
		Extracts the date from receivedDate key in dict and parse in a format for monica api


		Parameters: 
		-----------
		date_time: datetime object
			datetime object from the gmail data
		

		Returns: 
		-------
		date: str
			Returns date in Format: YYYY-MM-DD.

		"""

		try:
			return date_time.strftime('%Y-%m-%d')
		except:
			return ""





