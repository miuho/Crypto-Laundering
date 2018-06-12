# btc_purchase.py
# purchase Bitcoin using coinbase API
#
# HingOn Miu

# https://developers.coinbase.com/api/v2
# https://github.com/coinbase/coinbase-python

import io
import pycurl
import random
import string
import json
import time
from coinbase.wallet.client import Client


# your secret blockchain.info wallet (see secret_wallet.py)
bitcoin_address_of_secret_wallet = ""

# USD amount to send to final target eg. "5000"
usd_amount = ""

# register coinbase account and enable API keys
# https://developers.coinbase.com/docs/wallet/api-key-authentication
coinbase_api_key = ""
coinbase_api_secret = ""



# create coinbase client with your credentials
client = Client(coinbase_api_key, coinbase_api_secret)


# fetch default account ID from your coinbase account
print(term.format("Fetch Account Info\n", term.Attr.BOLD))
accounts_response = client.get_accounts()
print(term.format(accounts_response, term.Color.BLUE))
account_id = json.loads(accounts_response)["data"][0]["id"]


# check real time bitcoin price (total USD to buy one bitcoin)
print(term.format("Check Bitcoin Price\n", term.Attr.BOLD))
bitcoin_price_response = client.get_buy_price(currency_pair = 'BTC-USD')
print(term.format(bitcoin_price_response, term.Color.BLUE))
bitcoin_price = float(json.loads(bitcoin_price_response)["data"]["amount"])


# convert USD amount to bitcoin
bitcoin_amount = str(usd_amount / bitcoin_price)


# fetch default payment method ID from your coinbase account
print(term.format("Fetch Payment Method\n", term.Attr.BOLD))
payment_methods_response = client.get_payment_methods()
print(term.format(payment_methods_response, term.Color.BLUE))
payment_method_id = json.loads(payment_methods_response)["data"][0]["id"]


# buy bitcoin and commit order immediately
print(term.format("Purchase Bitcoin\n", term.Attr.BOLD))
buy_response = client.buy(account_id, amount=bitcoin_amount, currency="BTC",
                          commit= True, payment_method=payment_method_id)
print(term.format(buy_response, term.Color.BLUE))


# verify purchase time
buy_time = json.loads(buy_response)["data"]["payout_at"]
print(term.format("Purchased Bitcoin at " + buy_time + "\n", term.Attr.BOLD))


# send purchased bitcoin to your secret blockchain.info wallet (see secret_wallet.py)
print(term.format("Transfer Bitcoin to Secret Wallet\n", term.Attr.BOLD))
transaction_response = client.send_money(account_id, to=bitcoin_address_of_secret_wallet, 
                                         amount=bitcoin_amount, currency='BTC')
print(term.format(transaction_response, term.Color.BLUE))
transaction_id = json.loads(transaction_response)["data"]["id"]
transaction_status = json.loads(transaction_response)["data"]["status"]


# keep checking until transaction is completed
print(term.format("Check Transaction Status\n", term.Attr.BOLD))
while transaction_status != "completed":
  # check status every 5 seconds
  time.sleep(5)
  transaction_response = client.get_transaction(account_id, transaction_id)
  transaction_status = json.loads(transaction_response)["data"]["status"]
  print(term.format(transaction_status + "\n", term.Attr.BOLD))


# alert transaction is completed
print(term.format("Bitcoin Transaction Completed\n", term.Attr.BOLD))




