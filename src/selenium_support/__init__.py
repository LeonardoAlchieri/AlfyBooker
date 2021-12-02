from typing import Dict, Callable, List, Any
from warnings import warn
from selenium import webdriver
from functools import wraps
from random import randrange
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
        building_name (str): building name for where to _book (must match name on website)
        room_name (str): room name inside the building selected (must match website as well)
    """
    def __init__(self, 
                 driver: WebDriver, 
                 username: str, 
                 password: str, 
                 url: str,
                 building_name: str,
                 room_name: str) -> None:
        """Constructor method
        """
        self.driver = driver
        self.credentials: Dict[str, str] = dict(username=username, 
                                                password=password)
        self.building_name = building_name
        self.room_name = room_name
        self.driver.get(url)
        
        
    def _select_deselect_frame(self, func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs) -> bool:
            self.driver.switch_to.frame(0)
            func(*args, **kwargs)
            self.driver.switch_to.default_content()
        return wrapper
    
    # TODO: look up if double decorator is fine
    @try_run_selenium_command
    @_select_deselect_frame
    def login_with_credential(self):
        """This method implements the main webpage login.
        """
        for frame, message in zip(self.driver.find_elements_by_id(id_ = 'login-input'), 
                                    self.credentials.values()):
            frame.send_keys(message)
        login_button = self.driver.find_element_by_xpath('//*[@id="Usa_le_tue_credenziali_di_Esse"]/form/button')
        login_button.click()        
        
    @try_run_selenium_command
    @_select_deselect_frame
    def platform_selection(self):
        """This method is used to select the webpage for the room booking.
        """
        aule_button = self.driver.find_element_by_xpath('//*[@id="AULE"]')
        aule_button.click()
        
    @staticmethod
    @try_run_selenium_command
    def find_all_available_slots(driver: WebDriver) -> List[Any]:
        return sorted([el 
                       for el in driver.find_elements_by_id('TESTO') 
                       if '/' not in el.text.split('\n')[-1]], 
                      key=lambda x: x.text)
        
    @try_run_selenium_command
    @_select_deselect_frame
    def set_number_of_slots(self):
        self.n_slots: int = sorted([el 
                                     for el in self.driver.find_elements_by_id('TESTO') 
                                     if '/' not in el.text.split('\n')[-1]], 
                                    key=lambda x: x.text)
        
    @try_run_selenium_command
    @_select_deselect_frame
    def _select_slot_from_idx(self, idx: int):
        slots_to_book = self.find_all_available_slots(driver=self.driver)
        slot = slots_to_book[idx]
        print(f'Pressing slot:\n{slot.text}')
        slot.click()
        
    @try_run_selenium_command
    @_select_deselect_frame
    def _select_building(self):
        buildings = self.driver.find_elements_by_id('EDIFICIO')
        matching_buildings = [building for building in buildings if building.text == self.building_name]
        if len(matching_buildings) == 1:
            building = matching_buildings[0]
            building.click()
        elif len(matching_buildings) > 1:
            warn(f'More building elements were found to match for the given name. Found: {matching_buildings}. Selecting first.')
            building = matching_buildings[0]
            building.click()
        else:
            raise RuntimeError(f'Could not find desired building: {self.building_name}')
        
    @try_run_selenium_command
    @_select_deselect_frame
    def _select_room(self):
        wanted_slot = [slot 
               for slot in self.driver.find_elements_by_id('SLOT')
               if 'Edificio A SPAZIO STUDIO 1' in slot.text]
        if len(wanted_slot) > 1:
            warn('More slots with the desired name.')
            wanted_slot = wanted_slot[0]
        elif len(wanted_slot) == 0:
        #     TODO: use something different then value error
            warn('No slot with the desired name. Random one will be chosen.')
            all_slots = [slot for slot in self.driver.find_elements_by_id('SLOT')]
            rand_idx = randrange(start=0, stop=len(all_slots))
            wanted_slot = all_slots[rand_idx]
        else:
            wanted_slot = wanted_slot[0]
        wanted_slot.click()

    @try_run_selenium_command
    @_select_deselect_frame
    def _book(self):
        self.driver.find_element_by_id('PRENOTA').click()
        if self.driver.find_element_by_id('Prenotazione_Effettuata'):
            print('Booking Completed for the indicated slot!')
            self.driver.find_element_by_id('GRAZIE').click()
        else:
            raise RuntimeError('Something went wrong: I could not confirm the booking.')
    
    def loop_over_all_slots_and_book(self):
        # NOTE: I use a loop over index instead of 
        for i in range(self.n_slots):
            print(f'Current slot selection: {i+1}/{self.n_slots}')
            self._select_slot_from_idx(idx=i)
            self._select_building()
            self._select_room()
            self._book()