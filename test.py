from math import log


def calc_doubling_time(percent_7day: float) -> float:
    """ convert 7-day-increase of incidence into doubling time"""
    tD = -7/log((1/(percent_7day+1)), 2)
    return tD


# print(calc_doubling_time(percent_7day=0.25))

l = range(0, 175, 25)
print(list(l))
