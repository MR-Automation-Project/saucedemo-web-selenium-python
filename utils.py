"""utils.py : action helper umum yang bisa digunakan pada layer : test class, pages, dan basemethod"""

import logging
import os
import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_element_to_be_visible(driver, locator, waitTime=6):
    """Menunggu hingga elemen terlihat."""
    try:
        element = WebDriverWait(driver, waitTime).until(EC.visibility_of_element_located(locator))
        return element
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Element not visible: {e}")
        return None  # Mengembalikan None jika elemen tidak ditemukan

def take_screenshot(driver, name):
    """Mengambil screenshot dan menyimpannya dalam folder 'screenshots' """
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    timestamp = time.strftime("%Y%m%d_%H%M%S")  # Tambahkan timestamp
    screenshot_path = os.path.join(screenshot_dir, f"{name}_{timestamp}.png")
    driver.save_screenshot(screenshot_path)
    return screenshot_path  # Kembalikan path screenshot


def refresh_browser(driver):
    """Me-refresh halaman browser."""
    driver.refresh()

def scroll_down_page(driver):
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_DOWN)
    actions.perform()

def scroll_up_page(driver):
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_UP)
    actions.perform()

def accept_alert(driver):
    alert_msg = driver.switch_to.alert
    alert_msg.accept()

def dismiss_alert(driver):
    alert_msg = driver.switch_to.alert
    alert_msg.dismiss()

def switch_to_frame(driver, locator, waitTime=6):
    WebDriverWait(driver, waitTime).until(EC.frame_to_be_available_and_switch_to_it(locator))

def switch_to_default_frame(driver):
    driver.switch_to.default_content()

def move_to_element(driver, locator):
    actions = ActionChains(driver)
    actions.move_to_element(wait_for_element_to_be_visible(driver, locator)).perform()

def enter_keyboard(driver):
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER)
    actions.perform()

def click_back_browser(driver):
    driver.back()

def click_forward_browser(driver):
    driver.forward()