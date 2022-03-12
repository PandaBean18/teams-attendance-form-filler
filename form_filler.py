import time
import sys
import json 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


class FormsFiller:

    def __init__(self, url, fav_option):
        self.fav_option = fav_option
        self.config = json.load(open('parameters.json'))
        self.target_url = url 
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless') #ensure that GUI is off 
        self.chrome_options.add_argument('--no-sandbox')
        self.webdriver_service = Service('/home/raghapbean/chromedriver/stable/chromedriver') # Path to chromedriver 
        self.browser = webdriver.Chrome(service = self.webdriver_service, options = self.chrome_options)

    def log_in(self):
        self.browser.get(self.target_url)
        time.sleep(3) # Ensuring that the page is loaded properly 
        print(self.browser.title)
        mail_input = self.browser.find_element(By.NAME, 'loginfmt') 
        next_button = self.browser.find_element(By.ID, 'idSIButton9') 
        print('Logging in as ', self.config['username'], ', this may take a while.')
        mail_input.send_keys(self.config['username']) # Entering the email
        next_button.click() # redirects(?) to page for entering the pass

        time.sleep(5) 

        pass_input = self.browser.find_element(By.NAME, 'passwd')
        submit_button = self.browser.find_element(By.ID, 'idSIButton9')

        pass_input.send_keys(self.config['password']) # Entering the password 
        submit_button.click()

        time.sleep(5)

        # ms will ask you if you want to stay signed in
        submit = self.browser.find_element(By.ID, 'idSIButton9')
        submit.click()
        print('Logged in successfully')
        time.sleep(5)


    def fill_form(self):
        # I could not figure out a way to pin point the option with seleniums find_element method, so im looping through 
        # all the options till i find the one with same value as self.fav_option
        print('filling ', self.browser.title)
        input_elements = self.browser.find_elements(By.TAG_NAME, 'input')
        divs = self.browser.find_elements(By.TAG_NAME, 'div') # Not the most efficient way but ms forms use div with js code (probably)
                                                              # for submission of form. element.submit() does not work either.

        
        # looking for the correct option
        for option in input_elements:
            if option.get_attribute('value').lower() == self.fav_option.lower():
                option.click()
                break

        # looking for the correct div
        for div in divs:
            if div.get_attribute('textContent') == 'Submit': 
                print(div)
                div.click()

        print('Submitted the form successfully.')
        time.sleep(5)
        self.browser.quit()

