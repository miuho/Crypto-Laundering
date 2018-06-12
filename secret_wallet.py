# secret_wallet.py
# create blockchain.info wallet without exposing your IP
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
create_wallet_endpoint = "api/v2/create?"

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


def create_secret_wallet(blockchain_api_key):
  print(term.format("New Secret Wallet\n", term.Attr.BOLD))

  # generate a random password
  # https://pythontips.com/2013/07/28/generating-a-random-string/
  main_password = \
    ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(12)])

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

  # query blockchain to create wallet with onion url
  GET_request = onion_url + create_wallet_endpoint + "api_code=" + blockchain_api_key \
    + "&password=" + main_password

  response = query(GET_request)
  print(term.format(response, term.Color.BLUE))

  # new secret wallet, without your IP trace
  parsed_response = json.loads(response)

  # blockchain wallet identifier
  guid = parsed_response["guid"]
  # wallet bitcoin address
  address = parsed_response["address"]

  # stop Tor instance
  tor_process.kill()

  return (guid, main_password, address)


def create_usual_wallet(blockchain_api_key):
  print(term.format("New Usual Wallet\n", term.Attr.BOLD))

  # generate a random password
  # https://pythontips.com/2013/07/28/generating-a-random-string/
  main_password = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(12)])

  # query blockchain to create wallet with clearnet url
  GET_request = clearnet_url + create_wallet_endpoint + "api_code=" + blockchain_api_key \
    + "&password=" + main_password

  response = query(GET_request)
  print(term.format(response, term.Color.BLUE))

  # new wallet, with your IP trace
  parsed_response = json.loads(response)

  # blockchain wallet identifier
  guid = parsed_response["guid"]
  # wallet bitcoin address
  address = parsed_response["address"]

  return (guid, main_password, address)
