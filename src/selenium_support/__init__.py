from typing import Dict, Callable
from selenium import webdriver
from functools import wraps
from selenium.webdriver.chrome.webdriver import WebDriver

from src.utils import try_run_selenium_command

class PlaceBooker():
    """This class is used to perform all of the necessary methods for the 
    booking of correct slots in the given webplatform.
    
    Since this is a selenium model, it cannot be built with generalization in mind.
    Indeed, it is purely built for the indicated web platform (see README) and may 
    be broken if some changes happen

    Args:
        driver (WebDriver): webdriver initiated; while suggested a Chrome driver, the
        code has been tested with Safari as well
        username (str): username for the access to the private area
        password (str): password associated with the username
        url (str): url to the login webpage
    """
    def __init__(self, driver: WebDriver, username: str, password: str, url: str) -> None:
        """Constructor method
        """
        self.driver = driver
        self.credentials: Dict[str, str] = dict(username=username, 
                                                password=password)
        self.driver.get(url)
        
    def _select_delect_frame(self, func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs) -> bool:
            self.driver.switch_to.frame(0)
            func(*args, **kwargs)
            self.driver.switch_to.default_content()
        return wrapper
    
    # TODO: look up if double decorator is fine
    @try_run_selenium_command
    @_select_delect_frame
    def login_with_credential(self):
        """This method implements the main webpage login.
        """
        for frame, message in zip(self.driver.find_elements_by_id(id_ = 'login-input'), 
                                    self.credentials.values()):
            frame.send_keys(message)
        login_button = self.driver.find_element_by_xpath('//*[@id="Usa_le_tue_credenziali_di_Esse"]/form/button')
        login_button.click()
        
    @try_run_selenium_command
    @_select_delect_frame
    def platform_selection(self):
        """This method is used to select the webpage for the room booking.
        """
        aule_button = self.driver.find_element_by_xpath('//*[@id="AULE"]')
        aule_button.click()