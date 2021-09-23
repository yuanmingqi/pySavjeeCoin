<p align="center">
  <a href="" rel="noopener">
 <img src="https://github.com/yuanmingqi/pySavjeeCoin/tree/main/src/logo.png" alt="Project logo"></a>
</p>

<h3 align="center">pySavjeeCoin</h3>

<div align="center">

  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/Bulid-Passing-green.svg" alt="Passing">
  <img src="https://img.shields.io/badge/Hash-SHA--256-purple.svg" alt="SHA-256">

</div>

---

# Original Version
The original JavaScript version can be find in [SavjeeCoin](https://github.com/Savjee/SavjeeCoin) of master [Savjee](https://www.savjee.be/) .

# Features
- Simple proof-of-work algorithm
- Verify blockchain (to prevent tampering)
- Generate wallet (private/public key)
- Sign transactions

# Installation

- Get the repository with git:
```shell
git clone https://github.com/yuanmingqi/pySavjee.git
```

- Install the packages from PYPI:
```shell
pip install -r requirements.txt -i https://pypi.org/simple/ 
```

# Get Started
## Generate a keypair
```python
from src.keyGenerator import generateKeyPair

generateKeyPair(nbits=512, saveDir='./key', mark='my')
generateKeyPair(nbits=512, saveDir='./key', mark='his')
```

## Create a blockchain instance
```python
from src.blockchain import Blockchain, Transaction
from src.keyGenerator import loadKeyPair

pySavjeeCoin = Blockchain()
```

## Adding Transactions
```python
# Load keypair
myPublicKey, myPrivateKey = loadKeyPair('./key', mark='my')
hisPublicKey, hisPrivateKey = loadKeyPair('./key', mark='his')

print('INFO: MY PUBLIC KEY IS {}'.format(myPublicKey))
print('INFO: HIS PUBLIC KEY IS {}'.format(hisPublicKey))

tx1 = Transaction(myPublicKey, hisPublicKey, 10)
tx1.signTransaction(myPublicKey, myPrivateKey)
pySavjeeCoin.addTransaction(tx1, myPublicKey)
```

## Mining the block
```python
print('INFO: START MINING...')
pySavjeeCoin.minePendingTransactions(myPublicKey)
```

## Get the balance and check the chain
```python
tx2 = Transaction(myPublicKey, hisPublicKey, 20)
tx2.signTransaction(myPublicKey, myPrivateKey)
pySavjeeCoin.addTransaction(tx2, myPublicKey)
print('INFO: START MINING...')
pySavjeeCoin.minePendingTransactions(myPublicKey)

print('INFO: BALANCE OF {} is {}'.format(myPublicKey, pySavjeeCoin.getBalanceAddress(myPublicKey)))

print('INFO: THE CHAIN IS VALID? {}'.format(pySavjeeCoin.isChainValid(myPublicKey)))
```
