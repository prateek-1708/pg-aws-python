#!/usr/local/bin/python3

import boto3
import base64
import argparse
import json
import sys

# Init parser for command line args.
parser = argparse.ArgumentParser("Decrypt KMS encrypted string")
parser.add_argument("-e", "--encrypted-string", required=True,  help='KMS encrypted string that needs decrypting')
parser.add_argument("-p", "--print-plaintext", action='store_true', default=False,  help='KMS encrypted string that needs decrypting')
args = parser.parse_args()

# Get the session to get the region name;
session = boto3.session.Session()
awsRegion = session.region_name

# create the kms client to do the decrypttion
kmsClient = boto3.client('kms')

# base64 decode into a ciphertext blob
blob = base64.b64decode(args.encrypted_string)

# KMS decrypt
try:
	decrypted = kmsClient.decrypt(CiphertextBlob=blob)
except Exception as e:
	print(str(e))
	sys.exit(1)


# plaintext from the decrypted
plaintext = decrypted['Plaintext']


if (args.print_plaintext):
	print(" Are you alone ? No body staring at your monitor ? OK to print plaintext ? [y or n]", end='->  ', flush=True)
	userSays = sys.stdin.readline().rstrip('\n')
	print("++++++++++++++++++++ Plain Text Alert +++++++++++++++++++++")
	if (userSays == 'y'):
		print (str(plaintext, 'utf-8'))
		print ("You should definitely consult someone or may be print it on a t-shirt ")
	else:
		print("hmmmm good call")
else:
	# write plaintext to file.
	f = open('/tmp/plaintext', 'w')
	f.write(str(plaintext,'utf-8')) 
	f.close()


