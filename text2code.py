#text to code stuff here
def def_func(arr):
    print()
    #nothing here yet
def def_var(arr):
    print()
    #nothing here yet

call_the_func = {'the','a','function'}
call_on = {'on','the','argument','arguments','parameter','parameters'}
call_and = {'and', 'also', 'the', 'argument'}
def call(arr):
    code = '('
    i = 0
    while arr[i] in call_the_func:
        i+=1
    n_exp = expression(arr[i:])
    code += n_exp[0]+' '
    i += n_exp[1]
    while arr[i] in call_on:
        i+=1
    while arr[i] != 'stop':
        n_exp = expression(arr[i:])
        code += n_exp[0]+' '
        i += n_exp[1]
        while arr[i] in call_and:
            i+=1
    return (code.strip() + ')',i+1)
    

def skip(d, *strs):
    for s in strs:
        d[s]=d
def all_same(d, val, *keys):
    for k in keys:
        d[k] = val
def identity(d, *vals):
    for val in vals:
        d[val]=val
def_tree = {
    'function': def_func,
    'variable': def_var
}
skip(def_tree, 'a', 'an', 'the')

expr_start_tree = {
    'define': def_tree,     #dict
    'call': call,           #handler
    'calling': call,        #handler
    'one': '1',             #literal
    'zero': '0'             #literal
}
skip(expr_start_tree,'the','result','of')
all_same(expr_start_tree,'+','plus','add')
identity(expr_start_tree,'+','0','1')
def expression(arr):
    i = 0
    res = expr_start_tree
    while isinstance(res, dict):
        #print('e',arr,i)
        res = res[arr[i]]
        i += 1
    if isinstance(res, str):
        return (res,1)
    return res(arr[i:])
    

def expr(string):
    return expression(string.split())
