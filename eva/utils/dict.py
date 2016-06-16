from collections import namedtuple


def convert(dictionary):
    '''(递归)转换字典对象为 namedtuple 对象
    '''

    for key, value in dictionary.items():
        if isinstance(value, dict):
            dictionary[key] = convert(value)
    return namedtuple('GenericDict', dictionary.keys())(**dictionary)

# 一个别名
dict_to_namedtuple = convert
