# Extended 721
This python script allows you to query onchain payloads and references using the blockfrost api

## Before you start
* You will basic python knowlege to run
* A mainnet or testnet https://blockfrost.io/ api key
* A policy hash
* The mint hash of the nft you want to verify

The default example demonstrates this on the https://bitbots.art nft

## What is going on
* The Cardano chain currently [06/15/2022] allows for 16kB of data to be stored in one transaction
* To bypass this limitation we use payloads and references
* This script will query the chain for all payloads
* Then query a specific mint tx for references
* With this data we can then output a file with the correct data