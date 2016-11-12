#text to code stuff here
def def_func(arr):
    print()
    #nothing here yet
def def_var(arr):
    print()
    #nothing here yet

call_the_func = {'the','a','function'}
call_replace = {'plus':'+','add':'+'}
call_on = {'on','the','argument','arguments','parameter','parameters'}
call_and = {'and', 'also', 'the', 'argument'}
def call(arr):
    code = '('
    i = 0
    while arr[i] in call_the_func:
        i+=1
    if arr[i] in call_replace:
        code += call_replace[arr[i]]+' '
    else:
        code += arr[i]+' '
    i+=1
    while arr[i] in call_on:
        i+=1
    while arr[i] is not 'stop':
        code += expression(arr[i:])
        while arr[i] in call_and:
            i+=1
    return code +')'
    

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
