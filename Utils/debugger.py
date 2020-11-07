import time
from Utils.arguments import Arguments


def debugger(original_function):
    def new_function(*args, **kwargs):
        if not Arguments().debug:
            return original_function(*args, **kwargs)
        result = original_function(*args, **kwargs)
        time.sleep(1)
        args = make_arguments(args)
        print('Function name: ', original_function.__name__, end='. ')
        print('Arguments: ', args)
        print('Returned value: ', result)
        return result
    return new_function


def make_arguments(args):
    reformat_args = []
    for i in range(1, len(args)):
        if isinstance(args[i], bytes):
            reformat_args.append('binary data')
    return reformat_args
