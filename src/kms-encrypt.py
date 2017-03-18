#!/usr/local/bin/python3

import boto3
import argparse
import sys
import os
import base64

sys.path.append(os.getcwd())
from helper import expiry


##############################################################################
def read_arguments():
    parser = argparse.ArgumentParser("Encrypt plaintext with KMS")
    parser.add_argument(
        "-p",
        "--plaintext",
        required=True,
        help='Plaintext string to be encrypted'
    )
    parser.add_argument(
        "-k",
        "--key-id",
        required=True,
        help='KMS key id to use'
    )
    args = parser.parse_args()

    if not args.plaintext:
        parser.error("I mean you need to pass something to encrypt")

    if not args.key_id:
        parser.error("Key to use to encrypt")

    return args


##############################################################################
def main():
    # Init parser for command line args.
    pass_args = read_arguments()

    # Get the session to get the region name;
    session = boto3.session.Session()
    aws_region = session.region_name

    # create the kms client to do the decryption
    kms_client = boto3.client('kms')

    # KMS decrypt
    try:
        encrypted = kms_client.encrypt(
            KeyId=pass_args.key_id,
            Plaintext=pass_args.plaintext
        )
    except Exception as e:
        print(str(e))
        print(aws_region)
        print("Credentials expire at: " + expiry.aws_creds_expiry())
        sys.exit(1)

    # plaintext from the decrypted
    encrypted = base64.b64encode(encrypted['CiphertextBlob'])
    print(str(encrypted, 'utf-8'))


##############################################################################
if __name__ == '__main__':
    main()
