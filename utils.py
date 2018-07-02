'''A collection of misc. functions.'''


def read_csv(fn, delimiter='\t'):
    '''Return a list of dictionaries with the contents of the file.

    Assumes newline characters at the end of each line, which are trimmed.'''

    objects = []
    with open(fn, 'r') as inf:
        iterator = inf.readlines()
        header = iterator[0]
        fields = header[:-1].split(delimiter)

        for line in iterator[1:]:
            objects.append({k: v for k, v in zip(fields, line[:-1].split(delimiter))})
    
    return objects


def refactor_json_data(json_list, master_key):
    '''Refactor a json list into a dictionary using
    the key `key` from each dictionary in the list.

    >>> refactor_json_data([{'id': 1, 'data': 'stuff'},
                            {'id': 2, 'data': 'things}])
    {1: {'data': 'stuff'}, 2: {'data': 'things'}}

    This is useful for fast lookups.'''

    out_dict = {}
    for item in json_list:
        uid = item.pop(master_key)
        out_dict[uid] = item

    return out_dict