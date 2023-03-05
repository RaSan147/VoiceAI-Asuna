import time
from datetime import datetime
import pytz



def utc2local(utc_dt):
	epoch = time.mktime(utc_dt.timetuple())
	offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
	return utc_dt + offset
	
def local2bd_time(time):
	return datetime.fromtimestamp(time, tz=pytz.timezone('Asia/Dhaka'))
	
def local2bd_dt(dt=datetime.now()):
	dt = dt.astimezone(pytz.timezone('Asia/Dhaka'))
	
	return dt
	


def from_jstime(ms):
	return utc2local(ms/1000.0)
# parse js miliseconds to time

def utc_to_bd_time(utc_dt=None):
	if isinstance(utc_dt, (int, float)):
		utc_dt = datetime.utcfromtimestamp(utc_dt)

	_utc = utc_dt or datetime.utcnow()
	local = utc2local(_utc)
	bd = local2bd_dt(local)
	
	return bd
	

if __name__=="__main__":
	print(utc_to_bd_time(1677963222428/1000))

	print(datetime.fromtimestamp(1678025767196/1000))
