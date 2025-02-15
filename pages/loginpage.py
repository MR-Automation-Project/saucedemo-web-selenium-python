from basemethod import Basemethod
from dataconfig.testdata import TestData as TD
from selenium.webdriver.common.by import By

class LoginPageLocator:
    USERNAME = (By.ID, 'user-name')
    PASSWORD = (By.ID, 'password')
    LOGIN_BTN = (By.ID, 'login-button')

class LoginPageAction(Basemethod, LoginPageLocator):

    def __init__(self, driver):
        super().__init__(driver)

    def login_with_standart_user(self):
        self._input(self.USERNAME, TD.STANDARD_USERNAME)
        self._input(self.PASSWORD, TD.GENERAL_PASSWORD)
        self._click_on(self.LOGIN_BTN)

    def login(self, username, password):
        self._input(self.USERNAME, username)
        self._input(self.PASSWORD, password)
        self._click_on(self.LOGIN_BTN)