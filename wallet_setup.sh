#!/bin/sh

#https://github.com/blockchain/service-my-wallet-v3


# run install.sh to install blockchain.info wallet service
npm update -g blockchain-wallet-service
blockchain-wallet-service -V

# run blockchain.info wallet service locally
blockchain-wallet-service start --bind 0.0.0.0 --port 3000 --ssl-key key_loc --ssl-cert cert_loc
