from typing import Callable, Dict, Any
from yaml import safe_load as load_yaml
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

def load_config(path: str) -> Dict[str, Any]:
    """Simple method to load yaml configuration for a given script.

    Args:
        path (str): path to the yaml file

    Returns:
        Dict[str, Any]: the method returns a dictionary with the loaded configurations
    """
    with open(path, 'r') as file:
        config_params = load_yaml(file)
    return config_params