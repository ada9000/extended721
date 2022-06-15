from blockfrost import BlockFrostApi, ApiError, ApiUrls

class BlockFrostTools:
    def __init__(self, testnet:bool=False, apiKey:str=None):
        self.b_url = ApiUrls.mainnet.value
        if testnet:
            self.b_url = ApiUrls.testnet.value
        # get api key from .env
        if not apiKey:
            raise Exception("No blockfrost api key")
        # init api
        self.api = BlockFrostApi(
            project_id=apiKey,
            base_url=self.b_url
        )

        self.projectPayloads = {}
        self.nftNameTxs = {}

    def healthy(self):
        return self.api.health().is_healthy

    def payloads_from_policy(self, policyHash:str=None):
        """
        getPayloadsFromPolicy
        @policyHash = the target policy hash i.e "ba3afde69bb939ae4439c36d220e6b2686c6d3091bbc763ac0a1679c"
        retuns a dict containing all payload data

        Get all assets in a given policy
            Find all tx hashes for each asset
                Get all metadata from each tx
        
        With the obtained metadata search and append all payloads to a dic
        """
        if not policyHash:
            raise Exception("onChainDataFromPolicy requires a policyHash")

        if policyHash in self.projectPayloads.keys():
            print("Avoiding duplicate api call")
            return self.projectPayloads[policyHash]

        metaData = []
        payloads = {}
        txCount = 0
        try:
            page = 1
            pagesLeft = True
            while pagesLeft:
                assets = self.api.assets_policy(policyHash, page=page)
                if assets == []:
                    pagesLeft = False
                    break
                for asset in assets:
                    assetTx = self.api.asset_transactions(asset.asset)
                    for x in assetTx:
                        txCount += 1
                        metaData.append(self.api.transaction_metadata(x.tx_hash, return_type='json'))
                        print(f"Index at {txCount}", end='\r')
                page += 1
        except ApiError as e:
            print(f"ApiError '{e}'")

        for metas in metaData:
            for meta in metas:
                if meta['label'] != '721':
                    break
                try:
                    payload = meta['json_metadata']['payload']
                    for key in payload.keys():
                        payloads[key] = payload[key]
                except KeyError:
                    pass


        self.projectPayloads[policyHash] = payloads
        return payloads


    def nft_references_to_file(self, policyHash:str, nftMintTx:str, filePath:str=None):
        payloads = {}
        if policyHash not in self.projectPayloads.keys():
            payloads = self.payloads_from_policy(policyHash)
        else:
            payloads = self.projectPayloads[policyHash]

        meta = self.api.transaction_metadata(nftMintTx, return_type='json')
        nftName = list(meta[0]['json_metadata'][policyHash].keys())[0]
        references = meta[0]['json_metadata'][policyHash][nftName]['references']['src']

        data = ""
        for ref in references:
            for subdata in payloads[str(ref)]:
                data += subdata

        print(data)

        with open(filePath, "w") as f:
            print(data, file=f)