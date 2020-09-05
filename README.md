# monica-python
Connects to the Monica API and provides an easy to use python API.

This Repo is work in progress. Future plan is to integrate data from other social media and emails.

This is inspired from the this [repo](https://pypi.org/project/monica-client/).

Contribution needed for:
1. Other APIs to be converted to Python structure
2. Social Media Integrations


## Contacts API

1. Initating the conversations API
```python
from monica.contacts import Contacts
import pandas as pd

contacts = Contacts(access_token)
```

2. Lists a few contacts from the database with criteria

```python

limit=10 # default
page=1 # default
sort="updated_at" # default
json_data = contacts.list_contacts(self, limit=limit, page=page, sort=sort) # returns json data

pd.DataFrame(json_data['data'])

``` 

3. List all contacts (Save it as csv file for other features)

```python

sort = "updated_at" # default
json_data = conversations.list_all_your_contacts(sort=sort)

df = pd.DataFrame(json_data['data'])
df.to_csv('contacts_from_monicahq.csv')

```


## Conversations API

1. Initating the conversations API
```python
from monica.conversations import Conversations
import pandas as pd

conversations = Conversations(access_token)

```

2. Lists a few conversations from the database - Official API does not return all the conversations

```python

conversations.list_conversations()

```

3. Create conversation object

```python

conversation_id = conversations.create_conversation_object(happened_at, contact_field_type_id, contact_id)

```

4. Add message to a conversation object
```python

conversations.add_message(written_at, written_by_me, content, contact_id, conversation_id):

```

5. Lists all conversations of a contact
```python


json_response = conversations.list_conversations_of_a_contact(contact_id) # returns the whole json response from API.


pd.DataFrame(json_response['data']) # to see it properly in a dataframe format

```

6. Delete conversation
```python

conversations.delete_conversation(conversation_id)

```

7. Delete all conversations of a contact
```python

conversations.delete_all_conversations_of_a_contact(contact_id)

```

8. Add multiple messages to contact

```python

conversations.add_multiple_messages(contact_id, conversation_id, df) 
# df is pandas dataframe in a specific structure expected, will add later

```


Check out how to upload gmail data [here](examples/gmail.md)




