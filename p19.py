"""
You are given the following information, but you may prefer to do some research for yourself.

1 Jan 1900 was a Monday.
Thirty days has September,
April, June and November.
All the rest have thirty-one,
Saving February alone,
Which has twenty-eight, rain or shine.
And on leap years, twenty-nine.
A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.
How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?
"""
from datetime import datetime, timedelta

start_time = datetime.now()

op_date = datetime(1901, 1, 1)
last_date = datetime(2000, 12, 31)
sunday_firsts = 0

while op_date <= last_date:
    op_date += timedelta(days=1)
    if op_date.weekday() == 6 and op_date.day == 1:
        sunday_firsts += 1

print("Sundays on the first of a month in the 20th century: {}".format(sunday_firsts))
print("Execution time: {}".format(datetime.now() - start_time))
