#!/usr/bin/python3

import os
import sys
import time
import datetime
import struct
from time import mktime


def gettime(myTime):
    print(datetime(myTime.hour))
    return

try:
    awsCredsExpiry = int(os.environ['AWS_CREDS_EXPIRY'])
except:
    print("ERROR: Try to connect to AWS before you use this script...")
    sys.exit(1)

awsCredsExpiryTimestamp = time.strftime('%Y-%m-%d %a %H:%M:%S', time.localtime(awsCredsExpiry))


currentTimestamp=time.strftime('%Y-%m-%d %a %H:%M:%S', time.localtime())
currentTime = time.time()

delta = round((awsCredsExpiry - currentTime), 0)

if delta <= 0:
    print("\nCredentials have expired on: {} :(".format(awsCredsExpiryTimestamp))
else:
    print("Current time:                   {}".format(currentTimestamp))
    print("Credentials will expire on:     {}".format(awsCredsExpiryTimestamp))
    print("You still have some time left:  {}".format(str(datetime.timedelta(seconds=delta))))