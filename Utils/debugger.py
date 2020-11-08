import time
from Utils.arguments import Arguments

TAB_1 = '\t'


def debug_decorator(original_function):
    def new_function(*args, **kwargs):
        if not Arguments().debug:
            return original_function(*args, **kwargs)
        result = original_function(*args, **kwargs)
        time.sleep(Arguments().debug_wait)
        reformat_args = ReformatArguments(args, result)
        reformat_func_args = reformat_args.get_reformat_function_arguments()
        reformat_returned_value = reformat_args.get_reformat_returned_value()
        print('Function name:', original_function.__name__)
        print(TAB_1, 'Arguments:', reformat_func_args)
        print(TAB_1, 'Returned value:', reformat_returned_value, '\n')
        return result
    return new_function


class ReformatArguments:
    def __init__(self, function_arguments, returned_value):
        self._function_args = function_arguments
        self._returned_value = returned_value
        self._reformat_args = []
        self._update()

    def _update(self):
        self._reformat(self._function_args)
        self._function_args = self._reformat_args
        self._reformat_args = []
        self._make_returned()

    def get_reformat_function_arguments(self):
        return self._function_args

    def get_reformat_returned_value(self):
        return self._returned_value

    def _reformat(self, args):
        if not isinstance(args, tuple):
            args = [args]
        for arg in args:
            if isinstance(arg, bytes):
                self._reformat_args.append('binary data')
                continue
            if str(arg).find('object at') != -1:
                reformat_obj_string = self._reformat_objects(arg)
                self._reformat_args.append(reformat_obj_string)
                continue
            self._reformat_args.append(arg)

    def _make_returned(self):
        if self._returned_value:
            self._reformat(self._returned_value)
            self._returned_value = self._reformat_args
        else:
            self._returned_value = 'void function'

    @staticmethod
    def _reformat_objects(obj):
        string = str(obj)
        index = string.find('at')
        return string[1: index - 1]
