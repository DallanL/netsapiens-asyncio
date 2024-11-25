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


#USAGE

###Authentication:

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
from modules.auth import NetsapiensAPI

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
```

example response:
```bash
{'username': '123@testdomain.com', 'user': '123', 'territory': 'MainReseller', 'domain': 'testdomain.com', 'department': 'n/a', 'uid': '123@testdomain.com', 'login': '123@testdomain.com', 'scope': 'Super User', 'user_email': 'Hu.Man@DefinitlyNormal.com', 'displayName': 'Hu Man', 'access_token': '58c030a319224f69a5fd770995a0af0a', 'expires_in': 3600, 'token_type': 'Bearer', 'refresh_token': 'af329eb2aa6247739240af7b692ab02a', 'client_id': 'supersecretclientid', 'apiversion': 'Version: 44.1.2', 'expires_at': '2024-11-25 19:15:22', 'api_url': 'https://api.example.com'}

```
