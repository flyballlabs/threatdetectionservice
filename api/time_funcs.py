'''
@summary: Provides utility functions for working with datetimes, timestamps, etc..
@author: devopsec
'''

from datetime import datetime

def convert_epoch_ts(ts_string):
    ''' convert epoch timestamp to human readable format '''

    # if contains millis, strip them
    if len(ts_string) > 10:
        millis = len(ts_string) - 10
        ts_string = ts_string[:-millis]
    ts = datetime.fromtimestamp(
        int(ts_string)
    ).strftime('%Y-%m-%d %H:%M:%S')
    return ts

# DEBUG
# print(convert_epoch_ts("1284101485020"))
# print(convert_epoch_ts("1284101485"))

# TODO add methods for converting to client local timezone
