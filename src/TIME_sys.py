import time
from datetime import datetime, timedelta, timezone
import pytz


def get_time_offset():
	utc = datetime.utcnow()
	local = datetime.now()

	return (local - utc).seconds


def utc2local(utc_dt):
	epoch = time.mktime(utc_dt.timetuple())
	offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
	return utc_dt + offset


def local2bd_time(ts):
	return datetime.fromtimestamp(ts, tz=pytz.timezone('Asia/Dhaka'))


def local2bd_dt(dt=datetime.now()):
	dt = dt.astimezone(pytz.timezone('Asia/Dhaka'))

	return dt


def ts2dt(ts=0.0, offset=0.0):
	tz = timezone(timedelta(seconds=offset))
	return datetime.fromtimestamp(ts, tz=tz)

# print(ts2dt(1678120166.487, 21600))


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


def get_utc_time():
	return datetime.utcnow().timestamp()


def get_local_time(dt=datetime.utcnow(), offset=0):
	return dt.timestamp() + offset


if __name__ == "__main__":

	t = datetime.utcfromtimestamp(get_utc_time())
	tz = timezone(timedelta(seconds=get_time_offset()))
	print("utc time", t)
	print("time zone", tz)
	print("local time", t.astimezone(tz))
	x = get_utc_time()
	print("utc  time", get_utc_time())
	print("time offset", get_time_offset())
	print(utc_to_bd_time(1677963222428/1000))

	print(datetime.fromtimestamp(1678025767196/1000))
