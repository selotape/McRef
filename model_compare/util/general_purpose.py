import time


def timed(f):
    def timed_func(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        print("\n%r took: %2.4f seconds" % (f.__name__, te - ts))
        return result

    return timed_func


def partition(seq, func):
    return (item for item in seq if func(item)), (item for item in seq if not func(item))
