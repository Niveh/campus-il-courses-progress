
MONTH_DAYS = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}


def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def gen_secs():
    return (i for i in range(60))


def gen_minutes():
    return gen_secs()


def gen_hours():
    return (i for i in range(24))


def gen_time():
    for hour in gen_hours():
        for minute in gen_minutes():
            for sec in gen_secs():
                yield "%02d:%02d:%02d" % (hour, minute, sec)


def gen_years(start=2019):
    while True:
        yield start
        start += 1


def gen_months():
    return (i for i in range(1, 13))


def gen_days(month, leap_year=True):
    if leap_year and month == 2:
        return (i for i in range(1, 30))

    return (i for i in range(1, MONTH_DAYS[month] + 1))


def gen_date():
    for year in gen_years():
        for month in gen_months():
            for day in gen_days(month, is_leap_year(month)):
                for time in gen_time():
                    yield "%02d/%02d/%d %s" % (day, month, year, time)


iters = 0
for d in gen_date():
    iters += 1
    if iters % 1000000 == 1:
        print(d)
