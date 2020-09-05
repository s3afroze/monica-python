## Syncing emails from Gmail

```python
from social.gmail_preprocessing import Preprocessing
from social.utils import Utils
from social.gmail_monica_client import Gmail_Monica_Client

my_email = ""
gmail_json_file_path=""
monica_contacts_file_path=""

gmail_preprocessing = Preprocessing(gmail_json_file_path, monica_contacts_file_path)
df_preprocessed = gmail_preprocessing.prepare_dataframe(my_email)


gmail_monica_client = Gmail_Monica_Client(access_token=access_token)
gmail_monica_client.upload_emails_to_monica(df_preprocessed)


```