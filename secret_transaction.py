# secret_transaction.py
# make Bitcoin transaction to address using blockchain.info without exposing your IP
#
# HingOn Miu

# https://blockchain.info/api/blockchain_wallet_api

import io
import pycurl
import random
import string
import json
import stem.process
from stem.util import term


# https://blog.blockchain.com/2014/12/03/improved-security-for-tor-users/
clearnet_url = "https://blockchain.info/"
onion_url = "https://blockchainbdgpzk.onion/"

# API endpoint
transaction_endpoint = "merchant/"
single_payment = "/payment?"
multiple_payments = "/sendmany?"
wallet_balance = "/balance?"
address_balance = "/address_balance?"
generate_new_address = "/new_address?"
all_active_addresses = "/list?"

# Tor socket port
SOCKS_PORT = 7000


# https://stem.torproject.org/
def query(url):
  output = io.BytesIO()

  # connect to webserver with pycurl
  query = pycurl.Curl()
  query.setopt(pycurl.URL, url)
  query.setopt(pycurl.PROXY, 'localhost')
  # use pycurl to fetch a site using the proxy on the SOCKS_PORT
  query.setopt(pycurl.PROXYPORT, SOCKS_PORT)
  query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
  query.setopt(pycurl.WRITEFUNCTION, output.write)

  try:
    query.perform()
    # return the query output from webserver
    return output.getvalue()
  # query failed with exception
  except pycurl.error as exc:
    return "Unable to reach %s (%s)" % (url, exc)


def print_bootstrap_lines(line):
  # print bootstrap info
  if "Bootstrapped " in line:
    print(term.format(line, term.Color.BLUE))


def make_secret_transaction(guid, password, from_address, satoshi_amount, to_address):
  print(term.format("New Secret Transaction\n", term.Attr.BOLD))

  # start Tor instance with exit node at Russia
  print(term.format("Starting Tor:\n", term.Attr.BOLD))

  tor_process = stem.process.launch_tor_with_config(
    timeout=300,
    config = {
      'SocksPort': str(SOCKS_PORT),
      #'ExitNodes': '{ru}',
    },
    init_msg_handler = print_bootstrap_lines,
  )

  # query blockchain to make payment with onion url
  GET_request = onion_url + transaction_endpoint + guid + single_payment \
    + "main_password=" + password + "&from=" + from_address \
    + "&amount=" + satoshi_amount + "&to=" + to_address

  response = query(GET_request)
  print(term.format(response, term.Color.BLUE))

  # new secret payment, without your IP trace
  parsed_response = json.loads(response)

  # response message
  message = parsed_response["message"]
  # additional message
  notice = parsed_response["notice"]
  # transaction hash
  tx_hash = parsed_response["tx_hash"]

  # stop Tor instance
  tor_process.kill()

  return tx_hash


def make_usual_transaction(guid, password, from_address, satoshi_amount, to_address):
  print(term.format("New Usual Transaction\n", term.Attr.BOLD))

  # query blockchain to make payment with clearnet url
  GET_request = clearnet_url + transaction_endpoint + guid + single_payment \
    + "main_password=" + password + "&from=" + from_address \
    + "&amount=" + satoshi_amount + "&to=" + to_address

  response = query(GET_request)
  print(term.format(response, term.Color.BLUE))

  # new payment, with your IP trace
  parsed_response = json.loads(response)

  # response message
  message = parsed_response["message"]
  # additional message
  notice = parsed_response["notice"]
  # transaction hash
  tx_hash = parsed_response["tx_hash"]

  return tx_hash


def check_secret_wallet_balance(guid, password):
  print(term.format("Check Secret Wallet Balance\n", term.Attr.BOLD))

  # start Tor instance with exit node at Russia
  print(term.format("Starting Tor:\n", term.Attr.BOLD))

  tor_process = stem.process.launch_tor_with_config(
    timeout=300,
    config = {
      'SocksPort': str(SOCKS_PORT),
      #'ExitNodes': '{ru}',
    },
    init_msg_handler = print_bootstrap_lines,
  )

  # query blockchain to check wallet balance with onion url
  GET_request = onion_url + transaction_endpoint + guid + wallet_balance \
    + "password=" + password

  response = query(GET_request)
  print(term.format(response, term.Color.BLUE))

  # check secret wallet balance, without your IP trace
  parsed_response = json.loads(response)

  # wallet balance in satoshi 
  balance = parsed_response["balance"]

  # stop Tor instance
  tor_process.kill()

  return balance


def check_secret_address_balance(guid, password, address):
  print(term.format("Check Secret Address Balance\n", term.Attr.BOLD))

  # start Tor instance with exit node at Russia
  print(term.format("Starting Tor:\n", term.Attr.BOLD))

  tor_process = stem.process.launch_tor_with_config(
    timeout=300,
    config = {
      'SocksPort': str(SOCKS_PORT),
      #'ExitNodes': '{ru}',
    },
    init_msg_handler = print_bootstrap_lines,
  )

  # query blockchain to check address balance with onion url
  GET_request = onion_url + transaction_endpoint + guid + address_balance \
    + "password=" + password + "&address=" + address 

  response = query(GET_request)
  print(term.format(response, term.Color.BLUE))

  # check secret address balance, without your IP trace
  parsed_response = json.loads(response)

  # address balance in satoshi 
  balance = parsed_response["balance"]

  # stop Tor instance
  tor_process.kill()

  return balance


def generate_secret_address_from_wallet(guid, password, address):
  # new address is secret only if secret wallet is used
  print(term.format("New Secret Address\n", term.Attr.BOLD))

  # start Tor instance with exit node at Russia
  print(term.format("Starting Tor:\n", term.Attr.BOLD))

  tor_process = stem.process.launch_tor_with_config(
    timeout=300,
    config = {
      'SocksPort': str(SOCKS_PORT),
      #'ExitNodes': '{ru}',
    },
    init_msg_handler = print_bootstrap_lines,
  )

  # query blockchain to generate new address with onion url
  GET_request = onion_url + transaction_endpoint + guid + generate_new_address \
    + "password=" + password

  response = query(GET_request)
  print(term.format(response, term.Color.BLUE))

  # generate new address, without your IP trace
  parsed_response = json.loads(response)

  # new address
  address = parsed_response["address"]

  # stop Tor instance
  tor_process.kill()

  return address



