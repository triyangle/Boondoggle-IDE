#text to code stuff here
def def_func(arr):
    #nothing here yet
def def_var(arr):
    #nothing here yet
def call(arr):
    #nothing here yet

def skip(d, *strs):
    for s in strs:
        d[s]=d

def_tree = {
    'function': def_func,
    'variable': def_var
}
skip(def_tree, 'a', 'an', 'the')

start_tree = {
    'define': def_tree,
    'call': call,
    'one': '1',
    '1': '1',
    'zero': '0',
    '0': '0'
}

def expression(arr):
    i = 0
    res = start_tree
    try:
        while isinstance(res, dict):
            res = res[arr[i]]
            i += 1
        if isinstance(res, str):
            return res
        return res(arr[i:])
    except IndexError as e:
        return arr
