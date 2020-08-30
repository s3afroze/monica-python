# monica-python
Connects to the Monica API and provides an easy to use python API.

This Repo is work in progress. Future plan is to integrate data from other social media and emails.

This is inspired from the this [repo](https://pypi.org/project/monica-client/).

Contribution needed for:
1. Other APIs to be converted to Python structure
2. Social Media Integrations

## Conversations API

1. Initating the conversations API
```python
from monica.conversations import Conversations

conversations = Conversations(access_token)
```

2. Lists a few conversations from the database - Official API does not return all the conversations

```python
from monica.conversations import Conversations

conversations.list_conversations()

```

3. Create conversation object

```python
from monica.conversations import Conversations

conversation_id = conversations.create_conversation_object(happened_at, contact_field_type_id, contact_id)

```

4. Add message to a conversation object
```python
from monica.conversations import Conversations

conversations.add_message(written_at, written_by_me, content, contact_id, conversation_id):

```

5. Lists all conversations of a contact
```python
from monica.conversations import Conversations
import pandas as pd

json_response = conversations.list_conversations_of_a_contact(contact_id) # returns the whole json response from API.


pd.DataFrame(json_response['data']) # to see it properly in a dataframe format

```

6. Delete conversation
```python
from monica.conversations import Conversations

conversations.delete_conversation(conversation_id)
```

7. Delete all conversations of a contact
```python
from monica.conversations import Conversations

conversations.delete_all_conversations_of_a_contact(contact_id)
```

8. Add multiple messages to contact

```python
from monica.conversations import Conversations

conversations.add_multiple_messages(contact_id, conversation_id, df) 
# df is pandas dataframe in a specific structure expected, will add later

```







## Syncing emails from Gmail

Find value of **my_name** variable on either **from_dict_name** or **to_dict_name** column name in the **gmail_df_cleaned.csv** file

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

