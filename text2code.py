
#text to code stuff here
func_params = {'with','parameter','parameters','param','params',
               'args','arg','arguments','argument','of'}
func_body = {'with','a','the','body','of','to','be','as','following'}
func_and = {'and','also','then'}

def def_func(arr):
    code = '(define ('
    i = 0
    code += arr[i]
    i+=1
    while arr[i] in func_params:
        i+=1
    while arr[i] not in func_body:
        code += ' '+arr[i]
        #print(code)
        i+=1
        while arr[i] in func_and:
            i+=1
    code += ")\n"
    while arr[i] in func_body:
        i+=1
    if arr[i] == 'just':
        i+=1
        while arr[i] in func_body:
            i+=1
        n_exp = expression(arr[i:])
        code += n_exp[0]+"\n"
        i += n_exp[1]
        return (code+')', i)
    else:
        while arr[i] != 'stop':
            n_exp = expression(arr[i:])
            code += n_exp[0]+"\n"
            i += n_exp[1]
        return (code+')', i+1)

var_body = {'with','a','the','body','of','to','be','as','following'}
def def_var(arr):
    code = '(define '
    i = 0
    code += arr[i]+' '
    i+=1
    while arr[i] in var_body:
        i+=1
    n_exp = expression(arr[i:])
    code += n_exp[0]
    i += n_exp[1]
    return (code+')', i+1)

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
    if arr[i] == 'just':
        i += 1
        n_exp = expression(arr[i:])
        code += n_exp[0]+' '
        i += n_exp[1]
        return (code.strip() + ')',i)
    else:
        while arr[i] != 'stop':
            n_exp = expression(arr[i:])
            code += n_exp[0]+' '
            i += n_exp[1]
            while arr[i] in call_and:
                i+=1
        return (code.strip() + ')',i+1)

def infix(arr):
    code = '(in '
    i = 0
    for _ in range(3):
        n_exp = expression(arr[i:])
        code += n_exp[0]+' '
        i += n_exp[1]
        #print(code)
    return (code.strip() + ')',i)

if_then = {'then'}
if_else = {'else','otherwise'}
def if_form(arr):
    code = '(if '
    i = 0
    n_exp = expression(arr[i:])
    code += n_exp[0]+'\n'
    i += n_exp[1]
    while arr[i] in if_then:
        i+=1
    n_exp = expression(arr[i:])
    code += n_exp[0]+'\n'
    i += n_exp[1]
    while arr[i] in if_else:
        i+=1
    n_exp = expression(arr[i:])
    code += n_exp[0]+'\n'
    i += n_exp[1]
    return (code+')', i)

def skip(d, *strs):
    for s in strs:
        d[s]=d
def all_same(d, val, *keys):
    for k in keys:
        d[k] = val
def identity(d, *vals):
    for val in vals:
        d[val]=val

call_the_func = {'the','a','function'}
call_on = {'on','the','argument','arguments','parameter','parameters','by'}
call_and = {'and', 'also', 'the', 'argument'}

gt_lt_skip = {'than','then','or','to'}
def gt_select(arr):
    i = 0
    while arr[i] in gt_lt_skip:
        i += 1
    if arr[i] != 'equal':
        return ('>',i)
    i+=1
    while arr[i] in gt_lt_skip:
        i += 1
    return ('>=',i)
def lt_select(arr):
    i = 0
    while arr[i] in gt_lt_skip:
        i += 1
    if arr[i] != 'equal':
        return ('<',i)
    i+=1
    while arr[i] in gt_lt_skip:
        i += 1
    return ('<=',i)

def_tree = {
    'function': def_func,
    'variable': def_var
}
skip(def_tree, 'a', 'an', 'the')

expr_start_tree = {
    'define': def_tree,     #dict
    'call': call,           #handler
    'calling': call,        #handler
    'within': infix,        #handler
    'if': if_form,          #handler
    'one': '1',             #literal
    'zero': '0'             #literal
}
skip(expr_start_tree,'the','result','of', 'by', 'is', 'than', 'to')
all_same(expr_start_tree,'+','plus','add')
all_same(expr_start_tree,'-','sub','subtract','minus','difference')
all_same(expr_start_tree,'*','mul','multiply','times','product')
all_same(expr_start_tree,'/','divide','quotient', 'divided')
all_same(expr_start_tree, '=','equal','equals')
all_same(expr_start_tree, gt_select,'greater','more')
all_same(expr_start_tree, lt_select,'less','smaller')

def expression(arr):
    i = 0
    res = expr_start_tree
    while isinstance(res, dict):
        #print('e',arr,i)
        if arr[i] in res:
            res = res[arr[i]]
        else:
            return (arr[i],i+1)
        i += 1
    if isinstance(res, str):
        return (res,i)
    n_res = res(arr[i:])
    return (n_res[0], n_res[1]+i)

#text to array
def text2arr(s):
    return s.split()

#error dictionary
errors = {
    ("it's",):("if",)
}

def fixtxterror(arr):
    phrases = choose(arr,3)
    for p in phrases:
        if p in errors:
            arr = replsub(arr,p,errors[p])
    arr = [elem.replace("'","") for elem in arr]
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
