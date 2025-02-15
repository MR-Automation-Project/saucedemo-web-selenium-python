from basemethod import Basemethod
from selenium.webdriver.common.by import By

class AboutPageLocator:
    SUBTEXT_IN_ABOUTPAGE = (By.XPATH, '//p[contains(@class, "css-1mz1i0z")]')

class AboutPageAction(Basemethod, AboutPageLocator):

    def __init__(self, driver):
        super().__init__(driver)

    def check_visibility_subtext_in_aboutpage(self):
        return self._is_element_visible(self.SUBTEXT_IN_ABOUTPAGE)