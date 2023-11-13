from web3 import Web3


mnemonics = []
with open('Data/Mnemonics.txt', 'r') as file:
    for i in file:
        mnemonics.append(i.rstrip())

def getPrivateKey():
    web3 = Web3(Web3.HTTPProvider('https://ethereum.publicnode.com'))

    for mnemonic in mnemonics:
        web3.eth.account.enable_unaudited_hdwallet_features()
        account = web3.eth.account.from_mnemonic(mnemonic)
        private_key = account.key.hex()

        print(account.address)

getPrivateKey()