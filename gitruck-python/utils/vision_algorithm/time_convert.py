
def sec2ts(secs):
    duration_temp = round(secs)
    _m, s = divmod(duration_temp, 60)
    h, m = divmod(_m, 60)
    duration = "%02d:%02d:%02d.00" % (h, m, s)
    return duration


class TimeConvert(object):

    def __init__(self):
        print(self)


if __name__ == "__main__":
    print(sec2ts(23234524))
