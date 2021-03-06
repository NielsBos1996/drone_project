import datetime
import functools
import tempfile
import time
import os

class MoveNotPossibleException(Exception):
    pass

def write_log(message: str, folder_name="drone_project"):
    assert isinstance(message, str)
    tempdir = f'{tempfile.gettempdir()}\\{folder_name}'
    if not os.path.isdir(f'{tempdir}'):
        os.mkdir(f'{tempdir}')
    with open(f'{tempdir}\\log.txt', 'a') as f:
        f.write(f'[{datetime.datetime.now()}] ' + message + '\n')


def execution_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        write_log(f'{func.__name__} called')
        st = time.time()
        result = func(*args, **kwargs)
        write_log(
            f'{func.__name__} finished, execution time={time.time() - st} '
            f'seconds')
        return result
    return wrapper

def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        args = ', '.join([str(elem) for elem in args])
        kwargs = ', '.join([f'{key}={value}' for key, value in kwargs.items()])
        write_log(f'{func.__name__}({args}{kwargs}) ->'
              f' {result}')
        return result
    return wrapper
