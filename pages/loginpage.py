from selenium.webdriver.common.by import By
from basemethod import Basemethod
from dataconfig.testdata import UserAccount as UA

class LoginPageLocator:
    USERNAME = (By.ID, 'user-name')
    PASSWORD = (By.ID, 'password')
    LOGIN_BTN = (By.ID, 'login-button')
    ERROR_MESSAGE = (By.XPATH, '//h3[@data-test="error"]')

class LoginPageAction(Basemethod, LoginPageLocator):

    def __init__(self, driver):
        super().__init__(driver)

    def input_username_field(self, username):
        self._clear_on_textbox(self.USERNAME)
        self._input(self.USERNAME, username)

    def input_password_field(self, password):
        self._clear_on_textbox(self.PASSWORD)
        self._input(self.PASSWORD, password)

    def clear_all_field(self):
        self._clear_on_textbox(self.PASSWORD)
        self._clear_on_textbox(self.USERNAME)

    def click_login_button(self):
        self._click_on(self.LOGIN_BTN)

    def get_error_message(self):
        error_msg = self._get_text_element(self.ERROR_MESSAGE)
        return error_msg

    def login(self, username, password):
        self.input_username_field(username)
        self.input_password_field(password)
        self.click_login_button()

    def login_with_standart_user(self):
        self._input(self.USERNAME, UA.STANDARD_USER)
        self._input(self.PASSWORD, UA.GENERAL_PASSWORD)
        self.click_login_button()

