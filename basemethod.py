import logging
import os
import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Basemethod:

    waitTime = 6

    def __init__(self, driver):
        self.driver = driver

    def _click_on(self, locator):
        try:
            if isinstance(locator, tuple):
                WebDriverWait(self.driver, self.waitTime).until(EC.element_to_be_clickable(locator)).click()
            elif isinstance(locator, WebElement):
                locator.click()
            else:
                raise ValueError("Invalid input locator. please give tuple format or WebElement instance")
                # Handling Tuple --> (By.Xpath, '//div[@class="user"]'
                # Handling WebElement  --> driver.find_element(By.ID, 'login-button')
        except(TimeoutException, NoSuchElementException) as e:
            logging.error(f"Error while clicking element: {e}")
        except Exception as e:
            logging.error(f"Error saat mengklik elemen: {e}")

    def _input(self, locator, input_text):
        element = WebDriverWait(self.driver, self.waitTime).until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(input_text)

    def _clear_on_textbox(self, locator):
        WebDriverWait(self.driver, self.waitTime).until(EC.visibility_of_element_located(locator)).clear()

    def _is_element_visible(self, locator):
        element = WebDriverWait(self.driver, self.waitTime).until(EC.visibility_of_element_located(locator))
        return bool(element)

    def _get_element(self, locator):
        element = WebDriverWait(self.driver, self.waitTime).until(EC.visibility_of_element_located(locator))
        return element

    def _get_text_element(self, locator):
        element = WebDriverWait(self.driver, self.waitTime).until(EC.visibility_of_element_located(locator))
        return element.text

    def _get_attribute_element(self, locator, attrib):
        attribute = WebDriverWait(self.driver, self.waitTime).until(EC.visibility_of_element_located(locator)).get_attribute(attrib)

    def _drag_and_drop(self, input_source_locator, input_target_locator):
        actions = ActionChains(self.driver)
        source = self._get_element(input_source_locator)
        target = self._get_element(input_target_locator)
        actions.drag_and_drop(source, target).perform()

    def _switch_to_frame(self, locator):
        WebDriverWait(self.driver, self.waitTime).until(EC.frame_to_be_available_and_switch_to_it(locator))

    def _switch_to_default_frame(self):
        self.driver.switch_to.default_content()

    def _accept_alert_js(self):
        alert_msg = self.driver.switch_to.alert
        alert_msg.accept()

    def _enter_keyboard(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    def _click_back_browser(self):
        self.driver.back()

    def _click_forward_browser(self):
        self.driver.forward()

    def _get_length_all_elements(self, locator):
        element = WebDriverWait(self.driver, self.waitTime).until(EC.visibility_of_all_elements_located(locator))
        return len(element)

    def _move_to_element(self, locators):
        actions = ActionChains(self.driver)
        actions.move_to_element(self._get_element(locators)).perform()

    def _scroll_down_page(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.PAGE_DOWN)
        actions.perform()

    def _scroll_up_page(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.PAGE_UP)
        actions.perform()

    def _select_dropdown_by_index(self):
        pass

    def _select_dropdown_by_value(self):
        pass

    def _get_current_url(self):
        time.sleep(5)
        actual_url = self.driver.current_url
        return actual_url

    def _capture_evidence(self, name):
        # Make sure the folder exists
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        screenshot_path = os.path.join(screenshot_dir, f"{name}.png")
        self.driver.save_screenshot(screenshot_path)