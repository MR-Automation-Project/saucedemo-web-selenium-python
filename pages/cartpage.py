from basemethod import Basemethod
from selenium.webdriver.common.by import By

class CartPageLocator:
    ITEM_NAME_IN_CART = (By.XPATH, '//div[@class="cart_item"]//div[@class="inventory_item_name" and text()="{}"]')

class CartPageAction(Basemethod, CartPageLocator):

    def __init__(self, driver):
        super().__init__(driver)

    def check_visibility_item_in_cart(self, product_name):
        formatted_xpath = self.ITEM_NAME_IN_CART[1].format(product_name)
        locator = (By.XPATH, formatted_xpath)
        check_item = self._is_element_visible(locator)
        return check_item