import logging
import time

from selenium.webdriver import ActionChains

from basemethod import Basemethod
from selenium.webdriver.common.by import By

class ProductsPageLocator:
    PAGEHEADER_TITLE = (By.XPATH, '//div[@class="header_secondary_container"]/span')
    HAMBURGERMENU_BTN = (By.XPATH, '//button[@id="react-burger-menu-btn"]')
    ABOUT_IN_HAMBURGER_MENU = (By.XPATH, '//a[text()="About"]')
    ADD_ITEM_TO_CART = (By.XPATH, '//div[text()="{}"]/ancestor::div[@class="inventory_item"]//button')
    CART_ICON = (By.XPATH, '//a[@data-test="shopping-cart-link"]')
    CART_BADGE = (By.XPATH, '//span[@data-test="shopping-cart-badge"]')

class ProductsPageAction(Basemethod, ProductsPageLocator):

    def __init__(self, driver):
        super().__init__(driver)

    def check_visibility_page_title_on_products_page(self):
        return self._is_element_visible(self.PAGEHEADER_TITLE)

    def add_product_to_cart(self, product_name):
        formatted_xpath = self.ADD_ITEM_TO_CART[1].format(product_name)
        locator = (By.XPATH, formatted_xpath)
        self._click_on(locator)
        time.sleep(1.5)

    def navigate_to_about_via_hamburgermenu(self):
        self._click_on(self.HAMBURGERMENU_BTN)
        self._click_on(self.ABOUT_IN_HAMBURGER_MENU)

    def click_cart_icon(self):
        self._click_on(self.CART_ICON)

    def get_count_on_cart_badge(self):
        try:
            count_badge = self._get_text_element(self.CART_BADGE)
            return int(count_badge)
        except:
            return 0