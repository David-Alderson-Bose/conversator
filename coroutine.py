
# Use this as a decorator for couritines
def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.__next__()
        return cr
    return start