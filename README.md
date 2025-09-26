# Introduction

This repo will contains all my scripts that import transactions from investments brokers (crypto, bank, etc)

## Installation for Python3

```sh
pipenv shell
pipenv install
```

OR

Windows:

```sh
python -m venv venv
./venv/Scripts/activate.ps1
pip install -r requirements.txt
```

```sh
cp settings.conf.example settings.conf
```

Modify values in file settings.conf and then launch your script on a previously downloaded transaction history csv.

```sh
python bitstack_app.py bitstack_2023.csv
```

## FAQ

### Where can I find my account_id ?

* Go to Ghostfolio.
* Click Accounts.
* Select your account where you want to import transactions.
* In your browser URL, you will see something like:
https://domain/en/accounts?accountId=<my_account_id_is_here>&accountDetailDialog=true
* It is in the URL

### What is my auth_bearer

That's the token you got when you first installed your server. It's a very long token

### Where did you get your Bitstack transaction history CSV

* On your mobile app, select Compte (or maybe Account)
* Documents
* Relevés de compte (or maybe Account reporting)
* Select the year or the month and then Export CSV.

### How do you manage Bitstack transactions import ?

Well, manually for the moment. I've asked an API key to Bitstack-app devs but it doesn't exist for now.
So it's sending reports to my email address and I will retrieve them manually. Maybe use paperless-ngx to consume automatically the CSV ?
Well, waiting for the API Key
