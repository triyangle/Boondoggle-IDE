
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

def detect_statement(arr):
    i = 0
    res = start_tree
    try:
        while not isinstance(res, str):
            res = res[arr[i]]
            i += 1
        return res
    except IndexError as e:
        return arr

#text to array
def text2arr(s):
    return s.split()

#error dictionary
errors = {
    
}

def fixtxterror(arr):
    phrases = choose(arr,3)
    for p in phrases:
        if p in errors:
            arr = replsub(arr,p,errors[p])
    return arr

#returns tuple of sublists of len at most n
def choose(arr, n):
    if not arr or not n:
        return
    for i in range(len(arr)-n+1):
        yield tuple(arr[i:i+n])
    yield from choose(arr,n-1)

#replaces every instance of sub within arr with new
def replsub(arr,sub,new):
    for i in range(len(arr)-len(sub)+1):
        if arr[i:i+len(sub)] == list(sub):
            arr = arr[:i] + list(new) + arr[i+len(sub):]
    return arr
