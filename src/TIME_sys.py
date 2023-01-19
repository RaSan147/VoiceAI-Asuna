import time
import datetime

# Get current time
# print(time.time())

def from_jstime(ms):
	return datetime.datetime.fromtimestamp(ms/1000.0)
# parse js miliseconds to time
