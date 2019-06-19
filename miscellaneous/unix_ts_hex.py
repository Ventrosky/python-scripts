import time, datetime

d2 = datetime.date(2013,1,29)
unixtime2 = time.mktime(d2.timetuple())
print('{:X}'.format(int(unixtime2)))
