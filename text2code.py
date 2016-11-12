#text to code stuff here
def skip(d, *strs):
    for s in strs:
        d[s]=d

def_tree = {
    'function': 'def_func',
    'variable': 'def_var'
}
skip(def_tree, 'a', 'an', 'the')

start_tree = {
    'define': def_tree,
    'call': 'call'
}

def detect_start(arr):
    i = 0
    res = start_tree
    try:
        while not isinstance(res, str):
            res = res[arr[i]]
            i += 1
        return res
    except IndexError as e:
        return arr
