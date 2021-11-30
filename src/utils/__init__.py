from typing import Callable
from functools import wraps
from warnings import warn

def try_run_selenium_command(func: Callable):
    """Wrapper method for the execution of selenium functions. What it 
    does is that instead of raising errors, it collects errors into warnings
    and return a bool depending on the output, that it `True` if the method 
    was successfull and `False` if it failed.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> bool:
        try:
            func(*args, **kwargs)
            return True
        except Exception as e:
            warn(f'The following error occurd while running th method: {func.__name__}: {e}')
            return False
    return wrapper