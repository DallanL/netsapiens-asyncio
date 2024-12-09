# netsapiens-asyncio

An asynchronous Python client library for the Netsapiens PBX APIv2, providing easy integration with your hosted PBX system.

## Installation

Install via pip:

```bash
pip install git+https://github.com/DallanL/netsapiens-asyncio.git
```

## Upgrade to latest library

Upgrade via pip:

```bash
pip install --upgrade git+https://github.com/DallanL/netsapiens-asyncio.git
```


# USAGE

## Authentication:

Create a dictionary with all needed authentication information and pass to the `NetsapiensAPI` class. then use the `get_token` method to return a dictionary containing all information about your token and other info to use that token with other API functions.

example authentication dictionary:
```bash
AUTH_CONFIG = {
    "base_url": "api.example.com",
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "username": "your_username",
    "password": "your_password",
}
```

example usage:

```bash
import asyncio
from netsapiens_asyncio.auth import NetsapiensAPI
async def main():

	# build authentication dictionary
	AUTH_CONFIG = {
	    "base_url": "api.example.com",
	    "client_id": "your_client_id",
	    "client_secret": "your_client_secret",
	    "username": "your_username",
	    "password": "your_password",
	}

	# Initialize the authentication client
	auth_client = NetsapiensAPI(AUTH_CONFIG)
	# Fetch the initial token
	response = await auth_client.get_token()

	print("Token Info:", response)

asyncio.run(main())

```

example response:
```bash
{'username': '123@testdomain.com', 'user': '123', 'territory': 'MainReseller', 'domain': 'testdomain.com', 'department': 'n/a', 'uid': '123@testdomain.com', 'login': '123@testdomain.com', 'scope': 'Super User', 'user_email': 'Hu.Man@DefinitlyNormal.com', 'displayName': 'Hu Man', 'access_token': '58c030a319224f69a5fd770995a0af0a', 'expires_in': 3600, 'token_type': 'Bearer', 'refresh_token': 'af329eb2aa6247739240af7b692ab02a', 'client_id': 'supersecretclientid', 'apiversion': 'Version: 44.1.2', 'expires_at': '2024-11-25 19:15:22', 'api_url': 'https://api.example.com'}
```

One authenticated, pass the response from `get_token()` to any other function for them to be properly authenticated.

## Messaging

### send_message
The `send_message` method allows you to send a message either to a new message session or to an existing session using the messagesession parameter.

Method Signature
```bash
async def send_message(
    self,
    message_type: str,
    message: str,
    destination: Union[str, list],
    from_number: str,
    messagesession: Optional[str] = None,
    data: Optional[str] = None,
    mime_type: Optional[str] = None,
    size: Optional[int] = None,
) -> dict
```
Parameters
message_type (str):
The type of message to send. Examples include:
- "sms": For text messages.
- "mms": For multimedia messages.

message (str):
The text content of the message to be sent.

destination (str | list):
The recipient of the message. This can be:
- A single phone number as a string.
- A list of phone numbers as a list of strings.

from_number (str):
The sender's phone number. Required for SMS.

messagesession (Optional[str]):
An optional session ID to send the message in. If provided, the ID:

- Must be at least 32 characters long.
- Must consist only of alphanumeric characters and underscores (_).
- If omitted, a new session will be created automatically.

data (Optional[str]):
Base64-encoded data for MMS or media messages.

mime_type (Optional[str]):
The MIME type of the media file for MMS or media messages (e.g., "image/jpeg").

size (Optional[int]):
The size of the media file in bytes.

#### Returns
A dictionary containing the API response.
#### Raises
ValueError: If the messagesession ID is invalid (does not meet the requirements).
Exception: If the API request fails or if authentication data is missing.

#### Example Usage
Send a New Message in a New Session
```bash
response = await message_client.send_message(
    message_type="sms",
    message="Hello, this is a test message!",
    destination="1234567890",
    from_number="1987654321",
)
print("Response:", response)
```

Send a Message in an Existing Session
```bash
response = await message_client.send_message(
    message_type="sms",
    message="This is a follow-up message in the session!",
    destination="1234567890",
    from_number="1987654321",
    messagesession="valid_session_id_with_32_or_more_characters_1234"
)
print("Response:", response)
```

Send an MMS Message
```bash
response = await message_client.send_message(
    message_type="mms",
    message="Here's a photo!",
    destination=["1234567890", "1987654321"],
    from_number="1234567899",
    data="base64_encoded_image_data",
    mime_type="image/jpeg",
    size=204800,  # 200 KB
)
print("Response:", response)
```
#### Behavior
If messagesession is provided and valid:
- The message is sent as part of the existing session.
If messagesession is omitted:
- A new session is created, and the message is sent within it.
All API calls are authenticated, and the token is refreshed if needed.
#### Validation
The messagesession parameter must:
- Be at least 32 characters long.
- Contain only alphanumeric characters and underscores (_).
Otherwise, a ValueError is raised.


## get_messages

The `get_messages` method retrieves message sessions or messages for a specific session from the Netsapiens API. It supports optional filtering by domain, user, and limit.

#### Method Signature

```bash
async def get_messages(
    self,
    messagesession: Optional[str] = None,
    domain: str = "~",
    user: Optional[str] = None,
    limit: Optional[int] = None,
) -> list[dict]
```

#### Parameters

domain (str):
- The domain to retrieve messages from.
- Defaults to "~", which refers to the domain linked to your token.

user (Optional[str]):
- The user to retrieve messages for.
- If omitted, retrieves sessions for the entire domain.

messagesession (Optional[str]):
- The session ID to retrieve messages for.
- If omitted, retrieves all message sessions for the given domain (or user, if provided).

limit (Optional[int]):
- Limits the number of sessions or messages retrieved.
- Defaults to no limit.

#### Returns
An Array of dictionaries:
- When messagesession is provided, each dictionary represents a message in the specified session.
- When messagesession is not provided, each dictionary represents a message session.

#### Raises
ValueError:
- If the messagesession ID is invalid (less than 32 characters or contains invalid characters).

Exception:
- If authentication fails or network/API errors occur.


#### Examples
Retrieve 50 Message Sessions for a Domain
```bash
response = await message_client.get_messages(
    domain="testdomain.com",
    limit=50,
)
print("Message Sessions:", response)
```

Retrieve All Message Sessions for a User
```bash
response = await message_client.get_messages(
    domain="2132560400.com",
    user="103",
)
print("User Message Sessions:", response)
```

Retrieve Messages for a Specific Session

```bash
response = await message_client.get_messages(
    messagesession="2d51df1810812ace8d138a2558d0bd79",
    domain="testdomain.com",
    user="123",
)
print("Messages in Session:", response)
```

# SubscriptionAPI Documentation

The `SubscriptionAPI` class provides methods to interact with the Netsapiens API for managing event subscriptions. It includes functionality to create, read, update, and delete subscriptions.

---

## **Initialization**

To use the `SubscriptionAPI` class, you need to initialize it with an authenticated instance of `NetsapiensAPI`.

### Example Initialization
```python
from netsapiens_asyncio.auth import NetsapiensAPI
from netsapiens_asyncio.subscribe import SubscriptionAPI
from config import AUTH_CONFIG

# Initialize the authentication client
auth_client = NetsapiensAPI(AUTH_CONFIG)

# Fetch the authentication token
await auth_client.get_token()

# Initialize the SubscriptionAPI client
subscription_client = SubscriptionAPI(auth_client)
```

### Methods

#### create_subscription

Creates a new event subscription.

Method Signature
```python
async def create_subscription(
    self,
    model: str,
    post_url: str,
    subscription_geo_support: Optional[str] = "yes",
    reseller: Optional[str] = "*",
    domain: Optional[str] = "*",
    user: Optional[str] = "*",
    preferred_server: Optional[str] = None,
) -> dict:
```

Example Usage
```python
response = await subscription_client.create_subscription(
    model="message",
    post_url="https://example.com/callback",
    subscription_geo_support="yes",
    domain="company.com",
    user="101",
    preferred_server="core1.nms-server.com"
)
print(response)
```

Expected Response
```json
{
    "id": "603559d421797c7b09b904ea9b6e6079",
    "model": "message",
    "post-url": "https://example.com/callback",
    "subscription-geo-support": "yes",
    "user": "101",
    "domain": "company.com",
    "preferred-server": "core1.nms-server.com",
    "status": "pending",
    "error-count": 0,
    "posts-count": 0,
    "subscription-creation-datetime": "2024-12-09T21:27:11+00:00",
    "subscription-expires-datetime": "2024-12-09T22:27:11+00:00"
}
```

---

#### read_subscription

Reads a subscription by its ID or fetches all subscriptions if no ID is provided.

Method Signature
```python
async def read_subscription(self, subscription_id: Optional[str] = None) -> Union[dict, list[dict]]:
```

Example Usage
Read a Specific Subscription
```python
response = await subscription_client.read_subscription(subscription_id="603559d421797c7b09b904ea9b6e6079")
print(response)
```

Read All Subscriptions
```python
response = await subscription_client.read_subscription()
print(response)
```

Expected Response
For a Specific Subscription
```json
{
    "id": "603559d421797c7b09b904ea9b6e6079",
    "model": "message",
    "post-url": "https://example.com/callback",
    "subscription-geo-support": "yes",
    "user": "101",
    "domain": "company.com",
    "preferred-server": "core1.nms-server.com",
    "status": "pending",
    "error-count": 0,
    "posts-count": 0,
    "subscription-creation-datetime": "2024-12-09T21:27:11+00:00",
    "subscription-expires-datetime": "2024-12-09T22:27:11+00:00"
}
```

---

#### update_subscription

Updates an existing subscription.

Method Signature
```python
async def update_subscription(
    self,
    subscription_id: str,
    model: Optional[str] = None,
    post_url: Optional[str] = None,
    subscription_geo_support: Optional[str] = None,
    subscription_expires_datetime: Optional[str] = None,
    preferred_server: Optional[str] = None,
    error_count: Optional[int] = None,
    posts_count: Optional[int] = None,
) -> dict:
```

Example Usage
```python
response = await subscription_client.update_subscription(
    subscription_id="603559d421797c7b09b904ea9b6e6079",
    model="cdr"
)
print(response)
```

Expected Response
```json
{
    "code": 202,
    "message": "Accepted"
}
```

---

#### delete_subscription

Deletes a subscription by its ID.

Method Signature
```python
async def delete_subscription(self, subscription_id: str) -> dict:
```

Example Usage
```python
response = await subscription_client.delete_subscription(subscription_id="603559d421797c7b09b904ea9b6e6079")
print(response)
```

Expected Response
```json
{
    "code": 202,
    "message": "Accepted"
}
```



