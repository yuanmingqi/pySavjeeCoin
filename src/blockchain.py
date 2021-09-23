import demjson
import hashlib
import random
import time
import rsa

class Transaction:
	def __init__(self, fromAddress, toAddress, amount, isGenesis=False):
		self.fromAddress = fromAddress
		self.toAddress = toAddress
		self.amount = amount

		if isGenesis:
			self.bill = {
				'fromAddress': self.fromAddress,
				'toAddress': self.toAddress,
				'amount': self.amount
			}
		else:
			if self.fromAddress is None:
				self.bill = {
					'fromAddress': self.fromAddress,
					'toAddress': self.toAddress.n,
					'amount': self.amount
				}
			else:
				self.bill = {
					'fromAddress': self.fromAddress.n,
					'toAddress': self.toAddress.n,
					'amount': self.amount
				}

	def calculateHash(self):
		message = str(self.fromAddress) + str(self.toAddress) + str(self.amount)
		hashValue = rsa.compute_hash(message.encode(), 'SHA-256')

		return hashValue

	def signTransaction(self, publicKey, privateKey):
		if publicKey != self.fromAddress:
			raise ValueError('YOU CAN NOT SIGN TRANSACTIONS FOR OTHER WALLETS!')

		hashTx = self.calculateHash()
		self.signature = rsa.sign_hash(hashTx, priv_key=privateKey, hash_method='SHA-256')

	def isValid(self, publicKey):
		if self.fromAddress == None:
			return True

		if (len(self.signature) == 0) or (bool(self.signature) is False):
			return ValueError('NO SIGNATURE IN THIS TRANSACTION!')

		message = str(self.fromAddress) + str(self.toAddress) + str(self.amount)
		result = bool(rsa.verify(message.encode(), self.signature, publicKey))

		return result


class Block:
	def __init__(self, timestamp, transactions, previousHash=''):
		self.timestamp = timestamp
		self.transactions = transactions
		self.previousHash = previousHash
		self.nonce = 0
		self.hash = self.calculateHash()

	def calculateHash(self):
		sha256 = hashlib.sha256()
		allBills = [trans.bill for trans in self.transactions]
		message = self.previousHash + str(int(self.timestamp)) + demjson.encode(allBills) + str(self.nonce)
		sha256.update(message.encode())
		hashValue = sha256.hexdigest()

		return hashValue

	def mineBlock(self, difficulty):
		# print(self.transactions)
		zeroString = ''.join(random.choice('0') for _ in range(difficulty))
		# print(zeroString, self.hash, self.hash[0:difficulty])
		while (self.hash[0:difficulty] != zeroString):
			self.nonce += 1
			self.hash = self.calculateHash()

		print('INFO: BLOCK SUCCESSFULLY MINED! HASH={}'.format(self.hash))

	def hasValidTransactions(self, publicKey):
		for trans in self.transactions:
			if trans.isValid(publicKey) is False:
				return False

		return True

class Blockchain:
	def __init__(self):
		self.chain = [self.createGenesisBlock()]
		self.difficulty = 2
		self.pendingTransactions = []
		self.miningReward = 100

	def createGenesisBlock(self):
		return Block(
			timestamp=time.time(),
			transactions=[Transaction(fromAddress='None', toAddress='Genesis Block', amount=0, isGenesis=True)],
			previousHash='0'
		)

	def getLatestBlock(self):
		return self.chain[-1]

	def minePendingTransactions(self, miningRewardAddress):
		rewardTx = Transaction(None, miningRewardAddress, self.miningReward)
		self.pendingTransactions.append(rewardTx)

		block = Block(timestamp=time.time(), transactions=self.pendingTransactions, previousHash=self.getLatestBlock().hash)
		block.mineBlock(self.difficulty)

		self.chain.append(block)

		self.pendingTransactions = []

	def addTransaction(self, transaction, publicKey):
		if (bool(transaction.fromAddress) is False) or (bool(transaction.toAddress) is False):
			raise ValueError('A TRANSACTION MUST INCLUDE FROM AND TO ADDRESS!')

		if transaction.isValid(publicKey) is False:
			raise ValueError('CANNOT ADD INVALID TRANSACTION TO THE CHAIN!')

		self.pendingTransactions.append(transaction)

	def getBalanceAddress(self, address):
		balance = 0.
		for block in self.chain:
			allBills = [trans.bill for trans in block.transactions]
			for bill in allBills:
				if bill['fromAddress'] == address.n:
					balance -= bill['amount']
				if bill['toAddress'] == address.n:
					balance += bill['amount']

		return balance

	def isChainValid(self, publicKey):
		for i in range(1, len(self.chain)):
			currentBlock = self.chain[i]
			previousBlock = self.chain[i - 1]

			''' check all the transactions '''
			if currentBlock.hasValidTransactions(publicKey) is False:
				return False

			''' check all the Hash values '''
			if currentBlock.hash != currentBlock.calculateHash():
				return False
			if currentBlock.previousHash != previousBlock.hash:
				return False

		return True
