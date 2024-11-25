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

### Authentication:

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

### Messaging

#### send_message
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
