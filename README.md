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

to send a message, once you have the auth dictionary you can start a new message using the `MessageAPI` class:


to send a message use `send_message()` (if you are continuing a previous message session, define the `messagesession`, otherwise a new session will be created)

```bash
import asyncio
from netsapiens_asyncio.auth import NetsapiensAPI
from netsapiens_asyncio.messages import MessageAPI

async def main():
	dst_number = "16265550123"
	src_number = "12135550123"

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


	# Initialize the message API client
	message_client = MessageAPI(auth_client)
	response = await message_client.send_message(
	    message_type="sms",
	    message="Hey, this is a test message via api!",
	    destination=dst_number,
	    from_number=src_number,
	)
	print("Message Response:", response)

asyncio.run(main())
```

