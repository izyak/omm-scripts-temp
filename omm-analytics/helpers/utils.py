##------------------##
##------UTILS-------##
##------------------##


def bytes_to_str(_byte):
    _byte = _byte[2:]
    _str = ""
    for i in range(0, len(_byte) - 1, 2):
        x = str(_byte[i]) + str(_byte[i + 1])
        _str += chr(int(x, 16))
    return _str


def get_unique_count(_dict):
    temp = [val for key, val in _dict.items()]  # 2D list
    unique_list = set([item for sublist in temp for item in sublist])
    return len(unique_list)


def get_total_count(_dict):
    _a = [v for k, v in _dict.items()]
    _wallets = []
    for i in _a:
        _temp = [v for k, v in i.items()]
        _wallets.extend([item for sublist in _temp for item in sublist])
    return len(set(_wallets))


def zero_if_none(n):
    return 0 if n is None else n
