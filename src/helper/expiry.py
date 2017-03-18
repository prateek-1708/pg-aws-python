import time
import os


##############################################################################
def aws_creds_expiry():
    return time.strftime('%Y-%m-%d %a %H:%M:%S', time.localtime(int(os.environ['AWS_CREDS_EXPIRY'])))