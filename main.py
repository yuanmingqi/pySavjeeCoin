from src.blockchain import Blockchain, Transaction
from src.keyGenerator import loadKeyPair

if __name__ == '__main__':
    pySavjeeCoin = Blockchain()
    myPublicKey, myPrivateKey = loadKeyPair('./key', mark='my')
    hisPublicKey, hisPrivateKey = loadKeyPair('./key', mark='his')

    print('INFO: MY PUBLIC KEY IS {}'.format(myPublicKey))
    print('INFO: HIS PUBLIC KEY IS {}'.format(hisPublicKey))

    tx1 = Transaction(myPublicKey, hisPublicKey, 10)
    tx1.signTransaction(myPublicKey, myPrivateKey)
    pySavjeeCoin.addTransaction(tx1, myPublicKey)
    print('INFO: START MINING...')
    pySavjeeCoin.minePendingTransactions(myPublicKey)

    tx2 = Transaction(myPublicKey, hisPublicKey, 20)
    tx2.signTransaction(myPublicKey, myPrivateKey)
    pySavjeeCoin.addTransaction(tx2, myPublicKey)
    print('INFO: START MINING...')
    pySavjeeCoin.minePendingTransactions(myPublicKey)

    print('INFO: BALANCE OF {} is {}'.format(myPublicKey, pySavjeeCoin.getBalanceAddress(myPublicKey)))

    print('INFO: THE CHAIN IS VALID? {}'.format(pySavjeeCoin.isChainValid(myPublicKey)))