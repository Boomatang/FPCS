key_pair = {'key.0': 'value0',
            'key.1': 'value1',
            'key.2': 'value2',
            'mail.0': 'mail0',
            'mail.1': 'mail1',
            'mail.2': 'mail2',
            'item': 'no value'}


def split_str(key_pair):
    """
    This function will a key pair in to a format that can be used to add more user to the system.
    :param key_pair:
    :return:
    """

    split_keys = key_pair.keys()
    for split_key in split_keys:
        key = split_key.split('.')
        if len(key) == 2:
            yield (key[1], key[0], key_pair.get(split_key))


def build_dict(items):
    """
    Takes a tuple of 3 to build a dict of added users.
    This could work for more but not yet.
    :param items: Works best if feed wit split_str()
    :return: dict of the vales entered
    """
    values = {}
    for i in items:
        if i[0] in values.keys():
            values[i[0]][i[1]] = i[2]
        else:
            values[i[0]] = {}
            values[i[0]][i[1]] = i[2]
    return values

if __name__ == '__main__':
    things = build_dict(split_str(key_pair))

    print(things)