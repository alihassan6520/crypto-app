# Flask Application

This is a Flask application that provides API endpoints for managing cryptocurrency addresses for users.
Supported Coins are Bitcoin and Ethereum.

## Table of Contents

1. [Directory Structure](#directory-structure)
2. [Installation and Setup](#installation-and-setup)
3. [Running Test Cases](#running-test-cases)
4. [API Usage](#api-usage)
5. [Generating RSA Keys](#generating-rsa-keys)
6. [Installing HashiVault and Saving Private Key](#installing-hashivault-and-saving-private-key)
7. [Docker](#docker)

## Directory Structure

The directory structure of the project is as follows:

├── app

│ ├── auth.py

│ ├── config.py

│ ├── data.db

│ ├── **init**.py

│ ├── models.py

│ ├── routes.py

│ └── utils.py

├── crypto

│ ├── address.py

│ └── **init**.py

├── run.py

└── tests

│ ├── test_app.py

- `app/`: Contains the Flask application code, including authentication, configuration, models, routes, and utility functions.
- `crypto/`: Contains cryptocurrency-related code, including the `generate_cryptocurrency_address` function.
- `run.py`: The entry point of the application.
- `tests/`: Contains the test cases for the application.

## Installation and Setup

(You can skip to Docker part)
To install and set up the application, follow these steps:

1. Clone the repository: `git clone <repository_url>`
2. Navigate to the project directory: `cd <project_directory>`
3. Create a virtual environment (optional but recommended): `python3 -m venv env`
4. Activate the virtual environment:
   - For Linux/Mac: `source env/bin/activate`
   - For Windows: `env\Scripts\activate.bat`
5. Install the required dependencies: `pip install -r requirements.txt`
6. Generate the RSA keys (see [Generating RSA Keys](#generating-rsa-keys) section for instructions).
7. Set up the configuration:
   - Copy the example configuration file: `cp app/config.py.example app/config.py`
   - Modify `app/config.py` file with your preferred settings.
8. Set up the database:
   - Initialize the database:
     `flask shell`
     
     `from app import db`
     
     `db.create_all()`
     
     This should be enough for this app. Also a sample data.db file is already provide you can skip.

9. To run the app type this command `flask run`

## Running Test Cases

To run the test cases, follow these steps:

1. Make sure the application and dependencies are installed (see [Installation and Setup](#installation-and-setup)).
2. Navigate to the project directory: `cd <project_directory>`
3. Activate the virtual environment (if not already activated).
4. Run the test command: `pytest tests`

## API Usage

The following are examples of curl commands to call the API endpoints:

1. Login:
   Test user already added

   ```shell
   curl --location --request POST 'http://localhost:5000/login' \
   --header 'Content-Type: application/json' \
   --data-raw '{"email": "test@example.com", "password": "testpassword123"}'
   ```

2. Generate Addresses (requires authentication):
   ```shell
   curl --location --request POST 'http://localhost:5000/addresses' \
   --header 'Authorization: <access_token>' \
   --header 'Content-Type: application/json' \
   --data-raw '{"cryptocurrency": "ETH"}'
   ```
3. List Addresses (requires authentication):

   ```shell
   curl --location --request GET 'http://localhost:5000/addresses' \
   --header 'Authorization: <access_token>'
   ```

4. Retrieve Address (requires authentication):
   ```shell
    curl --location --request GET 'http://localhost:5000/addresses/1' \
   --header 'Authorization: Bearer <access_token>'
   ```

Replace <access_token> with the actual access token obtained from the login API. This command will retrieve a list of addresses associated with the authenticated user.

Remember to make sure the Flask application is running on http://localhost:5000 or modify the command accordingly to match the correct host and port where the application is deployed.

## Generating RSA Keys

To generate public and pirvate key use:

```
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
```

```
openssl rsa -pubout -in private_key.pem -out public_key.pem
```

Keep private key in a secure place, like hasicorp vault, for more details see next step.
I already placed a public key in crypto/public.key
and stored one on Vault.
For this application (generating addresses) you only needs pubilc key.

## Installing HashiVault and Saving Private Key

First follow this to install vault for your system
https://developer.hashicorp.com/vault/downloads

After installation start the vault using command.

```
vault server -dev
```

When you will run the above command it will show the
url and a token.

export VAULT_ADDR='http://127.0.0.1:8200'

Visit http://127.0.0.1:8200 and in the token enter
the token that was shown when you started the vault.

In vault save the private key.

## Docker

Everything is setup inside docker so you dont need
to worry much.
After opening terminal in root directory of this project enter this command. Make sure docker is running.

```
docker build --tag python-docker .
```

After docker build just run this command and use above curl commands to call the apis.
A test db already added with default users which you can find in curl commands.

To start docker container run this.

```
docker run -d -p 5000:5000 python-docker
```

Now call the curl command to generate, list or retreive addresses.
