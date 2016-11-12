#text to array
def text2arr(s):
    return s.split()

#error dictionary
errors =
    {

    }

def fixtxterror(arr):
    lst = []
    [lst.extend([errors[e]]) if e in errors else lst.add(e) for e in arr]
    return lst
