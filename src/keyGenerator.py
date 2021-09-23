# -*- coding: utf-8 -*-
import rsa

def generateKeyPair(nbits, saveDir, mark):
	(pubkey, privkey) = rsa.newkeys(nbits)

	pub = pubkey.save_pkcs1()
	pubfile = open('{}/{}Public.pem'.format(saveDir, mark), 'wb')
	pubfile.write(pub)
	pubfile.close()


	pri = privkey.save_pkcs1()
	prifile = open('{}/{}Private.pem'.format(saveDir, mark), 'wb')
	prifile.write(pri)
	prifile.close()

	print('INFO: KEY PAIR SUCCESSFULLY GENERATED! SAVE DIR = {}'.format(saveDir))

def loadKeyPair(filePath, mark):
	with open('{}/{}Private.pem'.format(filePath, mark), mode='rb') as privateFile:
		privateKeyData = privateFile.read()
		privateFile.close()
	privateKey = rsa.PrivateKey.load_pkcs1(privateKeyData)

	with open('{}/{}Public.pem'.format(filePath, mark), mode='rb') as publicFile:
		publicKeyData = publicFile.read()
		publicFile.close()
	publicKey = rsa.PublicKey.load_pkcs1(publicKeyData)

	return publicKey, privateKey

# generateKeyPair(nbits=512, saveDir='./key', mark='my')
# generateKeyPair(nbits=512, saveDir='./key', mark='his')

# publicKey, privateKey = loadKeyPair('.')

# message = 'hello Bob!'.encode('utf-8')
# crypto = rsa.encrypt(message, pub_key=publicKey)
# print(crypto)
# message = rsa.decrypt(crypto, priv_key=privateKey)
# print(message.decode('utf-8'))

# hash = rsa.compute_hash(message, 'SHA-256')
# signature = rsa.sign_hash(hash, priv_key=privateKey, hash_method='SHA-256')
# print(signature)
#
# result = rsa.verify(message, signature, publicKey)
# print(result)