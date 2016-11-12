#text to code stuff here
def def_func(arr):
    print()
    #nothing here yet
def def_var(arr):
    print()
    #nothing here yet
def call(arr):
    print()
    #nothing here yet

def skip(d, *strs):
    for s in strs:
        d[s]=d

def_tree = {
    'function': def_func,
    'variable': def_var
}
skip(def_tree, 'a', 'an', 'the')

expr_start_tree = {
    'define': def_tree,     #dict
    'call': call,           #handler
    'one': '1',
    '1': '1',
    'zero': '0',
    '0': '0'
}

def expression(arr):
    i = 0
    res = expr_start_tree
    try:
        while isinstance(res, dict):
            res = res[arr[i]]
            i += 1
        if isinstance(res, str):
            return res
        return res(arr[i:])
    except IndexError as e:
        return arr
