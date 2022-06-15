from extended721 import Extended721

# some example data
API_KEY = "" # get a mainet key from from https://blockfrost.io/dashboard  (you will need an account)
BITBOT_0X0000_TX_HASH = "f43815fd35c813741712d027e0b5fb6462f3f60772fbeb342f501fc4b8e37991"
BITBOT_0X0094_TX_HASH = "439f506a187ebae0ac4697f79e1de2f160b33477e1fa317db1fa73dd19eb05c5"
BITBOTS_POLICY = "ba3afde69bb939ae4439c36d220e6b2686c6d3091bbc763ac0a1679c"

# query the blockchain and build the file
b = Extended721(apiKey=API_KEY)
b.nft_references_to_file(
    policyHash=BITBOTS_POLICY, 
    nftMintTx=BITBOT_0X0000_TX_HASH, 
    filePath="onchainNFT.svg"
    )