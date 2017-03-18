#!/usr/bin/env python3

import sys
import os
sys.path.append(os.getcwd())

from helper import expiry


print(expiry.aws_creds_expiry())