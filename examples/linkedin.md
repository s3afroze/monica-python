## Syncing conversations from Linkedin

```python
from social.linkedin_preprocessing import Preprocessing
from social.linkedin_monica_client import Linkedin_Monica_Client

linkedin_messages_file_path=""
monica_contacts_file_path=""

linkedin_preprocessing = Preprocessing(linkedin_messages_file_path, monica_contacts_file_path)
df_preprocessed = preprocessing.prepare_dataframe()


linkedin_monica_client = Linkedin_Monica_Client(access_token=access_token)
linkedin_monica_client.upload_conversations_to_monica(df_preprocessed)

```