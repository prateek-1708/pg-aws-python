#!/usr/local/bin/python3

import os
import time


##############################################################################
def main():
    aws_creds_expiry = int(os.environ['AWS_CREDS_EXPIRY'])

    aws_creds_expiry_timestamp = time.strftime('%Y-%m-%d %a %H:%M:%S', time.localtime(aws_creds_expiry))
    print("Cred Expire at ----> " + aws_creds_expiry_timestamp)

    current_timestamp = time.strftime('%Y-%m-%d %a %H:%M:%S', time.localtime())
    print("Time Now ----------> " + current_timestamp)

##############################################################################
if __name__ == '__main__':
    main()

