#!/usr/local/bin/python3

import boto3
import argparse
import sys
import os
import base64
import time


##############################################################################
def aws_creds_expiry():
    return time.strftime('%Y-%m-%d %a %H:%M:%S', time.localtime(int(os.environ['AWS_CREDS_EXPIRY'])))


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
        required=False,
        help='KMS key id to use'
    )
    args = parser.parse_args()

    if not args.plaintext:
        parser.error("Plaintext that needs encryption.")

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

    # now if key wasn't passed as arg lets ask the user which key they want to use
    if not pass_args.key_id:

        # get List of kms keys
        kms_response = kms_client.list_keys()

        # build a list of key ids
        keys = []
        for response_item in kms_response['Keys']:
            keys.append(response_item['KeyId'])
        option = get_user_selection(keys)
        key_id = keys[option - 1]
    else:
        key_id = pass_args.key_id

    # KMS decrypt
    try:
        encrypted = kms_client.encrypt(
            KeyId=key_id,
            Plaintext=pass_args.plaintext
        )
    except Exception as e:
        print(str(e))
        print("You are trying to decrypt in: {}".format(aws_region))
        print("Credentials expire at: {}".format(aws_creds_expiry()))
        sys.exit(1)

    # plaintext from the decrypted
    encrypted = base64.b64encode(encrypted['CiphertextBlob'])
    print(str(encrypted, 'utf-8'))


def get_user_selection(options):
    print("Following keys were found in the region / account combination:")
    for i, element in enumerate(options):
        print("{}) {}".format(i+1, element))
    i = input("Select a key to encrypt ")
    try:
        if 0 < int(i) <= len(options):
            return int(i)
    except:
        print("Please enter a valid choice")
    return None


##############################################################################
if __name__ == '__main__':
    main()
