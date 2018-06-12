# secret_mixing.py
# mix Bitcoin using privcoin.io without exposing your IP
#
# HingOn Miu

# https://www.privcoin.io/api/

import io
import pycurl
import random
import string
import json
import stem.process
from stem.util import term


# https://www.privcoin.io/bitcoin/
clearnet_url = "https://www.privcoin.io/"
onion_url = "http://tr5ods7ncr6eznny.onion/"

# API endpoint
get_mixing_address_endpoint = "bitcoin/api/?"
check_mixing_status_endpoint = "status/?"

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


def get_secret_mixing_address(forward_address):
  # forward_address is the receiver's Bitcoin address that you want to make
  # payment. privcoin then gives you a mixing address for you to send bitcoin. 
  # the bitcoin amount is mixed and ultimately forwarded to forward_address
  print(term.format("Get Secret Mixing Address\n", term.Attr.BOLD))

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

  # random time delay (0 - 24 hours) to reach forward_address
  #time_delay = "0"
  time_delay = str(random.randint(0,24))

  # minimum bitcoin transaction fee to pay privcoin
  minimum_service_fee = "0.8"

  # query privcoin to get mixing address with onion url
  GET_request = onion_url + get_mixing_address_endpoint + "addr1=" + forward_address \
    + "&pr1=100" + "&time1=" + time_delay + "&fee=" + minimum_service_fee

  response = query(GET_request)
  print(term.format(response, term.Color.BLUE))

  # new secret mixing address, without your IP trace
  parsed_response = json.loads(response)

  # check request status
  status = parsed_response["status"]
  if (status != "success"):
  	# alert request error message
  	message = parsed_response["message"]
  	# fix error before query again
  	print(term.format("Failed: " + message + "\n", term.Attr.BOLD))
  	return ""

  # request successful, parse mixing address
  mixing_address = parsed_response["address"]
  # privcoin mixing id
  mixing_id = parsed_response["bitcode"]

  # stop Tor instance
  tor_process.kill()

  return (mixing_address, mixing_id)


def check_secret_mixing_status(mixing_id):
  print(term.format("Check Secret Mixing Status\n", term.Attr.BOLD))

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

  # query privcoin to check mixing status with onion url
  GET_request = onion_url + check_mixing_status_endpoint + "id=" + mixing_id

  response = query(GET_request)
  print(term.format(response, term.Color.BLUE))

  # check secret mixing status, without your IP trace
  parsed_response = json.loads(response)

  # total bitcoin sent
  bitcoin_sent = parsed_response["totalBalance"]
  # total bitcoin remained
  bitcoin_remained = parsed_response["totalBalance"]

  print(term.format("Sent: " + bitcoin_sent + "\n", term.Attr.BOLD))
  print(term.format("Remained: " + bitcoin_remained + "\n", term.Attr.BOLD))

  # stop Tor instance
  tor_process.kill()

  return



