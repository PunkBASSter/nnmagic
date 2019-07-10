def calc_abs(lst):
    res = []
    for i in lst:
        res.append(abs(i))
    return res


def limit_by_amp(lst, limit):
    res = []
    for i in lst:
        sign = -1 if i<0 else 1
        res.append(i if abs(i) <= limit else limit * sign)
    return res


def scale_data(lst, k=None):
    res = []
    max_amp = k if k is not None else max(calc_abs(lst))
    for item in lst:
        res.append(item/max_amp)
    return res


def add_padding(lst, padding=0.0): #to synchronize normalized list size with original
    res = [padding, padding]
    res.extend(lst)
    return res
