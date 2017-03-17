#!/usr/local/bin/python3

import os
import time

awsCredsExpiry = int(os.environ['AWS_CREDS_EXPIRY'])

awsCredsExpiryTimestamp = time.strftime('%Y-%m-%d %a %H:%M:%S', time.localtime(awsCredsExpiry))
print(awsCredsExpiryTimestamp)


currentTimestamp=time.strftime('%Y-%m-%d %a %H:%M:%S', time.localtime())
print(currentTimestamp)
