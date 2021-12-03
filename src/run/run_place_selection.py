# PLEASE, RUN THIS SCRIPT FROM THE ROOT FOLDER OF THE REPO
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from os.path import abspath
from getpass import getpass
from sys import path
path.append('.')
from src.selenium_support import PlaceBooker
from src.utils import load_config


def main():
    print('-- Starting program. Loading config.')
    config = load_config(path=abspath('./src/run/config.yml'))
    print('-- Config successfully loaded.')
    print('-- Plase giver username and password.')
    # username = input('USERNAME: ')
    # password = getpass(prompt='PASSWORD: ')
    chrome_options = Options()
    chrome_options.add_argument('--lang=it-it')
    driver = webdriver.Chrome(executable_path=abspath("./chromedriver"),
                              options=chrome_options)
    place_booker = PlaceBooker(driver=driver,
                               username=config['username'],
                               password=config['password'],
                               url=config['url'],
                               building_name=config['building_name'],
                               room_name=config['room_name'])
    place_booker.login_with_credential()
    place_booker.platform_selection()
    place_booker.set_number_of_slots()
    place_booker.loop_over_all_slots_and_book()
    print('-- All possible booking were completed or some error occurd.')
    print('#### PROGRAM TERMINATED ####')

if __name__ == "__main__":
    main()