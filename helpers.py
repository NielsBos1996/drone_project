import functools
import tempfile
import time
import os

def write_log(message: str):
    assert isinstance(message, str)
    tempdir = f'{tempfile.gettempdir()}\\drone_project'
    if not os.path.isdir(f'{tempdir}'):
        os.mkdir(f'{tempdir}')
    with open(f'{tempdir}\\log.txt', 'a') as f:
        f.write(f'[{time.time()}] ' + message + '\n')


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