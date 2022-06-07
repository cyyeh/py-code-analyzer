import time


def conditonal_decorator(dec, condition):
    def decorator(func):
        if not condition:
            return func

        return dec(func)

    return decorator


def time_function(f):
    def wrapper(*args, **kwargs):
        begin = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f"function {f.__name__} took: {end - begin} seconds to execute.")
        return result

    return wrapper
