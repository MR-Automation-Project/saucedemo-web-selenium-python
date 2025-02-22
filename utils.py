"""
    utils.py : action helper umum yang bisa digunakan lebih luas.
                bisa digunakan pada layer : test class, pages, dan basemethod
"""

import logging
import os
import time
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_for_element_to_be_visible(driver, locator, waitTime=10):
    """Menunggu hingga elemen terlihat."""
    try:
        element = WebDriverWait(driver, waitTime).until(EC.visibility_of_element_located(locator))
        return element
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Element belum terlihat: {e}")
        return None  # Mengembalikan None jika elemen tidak terlihat

def wait_for_element_to_be_presence(driver, locator, waitTime=10):
    """Menunggu hingga elemen sudah tersedia di dalam DOM"""
    try:
        element = WebDriverWait(driver, waitTime).until(EC.presence_of_element_located(locator))
        return element
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Element belum tersedia di DOM: {e}")
        return None  # Mengembalikan None jika elemen tidak ditemukan di DOM

def wait_for_element_to_be_clickable(driver, locator, waitTime=10):
    """Menunggu hingga elemen sudah bisa diclicked"""
    try:
        element = WebDriverWait(driver, waitTime).until(EC.element_to_be_clickable(locator))
        return element
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Element belum dapat diclick: {e}")
        return None

def wait_for_frame_to_be_avail_and_switch_to_it(driver, locator, waitTime=10):
    try:
        element = WebDriverWait(driver, waitTime).until(EC.frame_to_be_available_and_switch_to_it(locator))
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

def click_back_browser(driver):
    driver.back()

def click_forward_browser(driver):
    driver.forward()

def accept_alert_prompt_browser(driver):
    alert_msg = driver.switch_to.alert
    alert_msg.accept()

def dismiss_alert_prompt_browser(driver):
    alert_msg = driver.switch_to.alert
    alert_msg.dismiss()

def press_enter_on_keyboard(driver):
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER)
    actions.perform()

def press_page_down_on_keyboard(driver):
    actions = ActionChains(driver).send_keys(Keys.PAGE_DOWN)
    actions.perform()

def press_page_up_on_keyboard(driver):
    actions = ActionChains(driver).send_keys(Keys.PAGE_UP)
    actions.perform()

def get_current_url(driver, url_contains_partial_text="", timeout=10):
    """
    Args:
        url_contains_partial_text: Bagian teks yang diharapkan ada dalam URL.
                                    Jika string kosong, maka hanya akan dicek apakah URL sudah ada
                                    (random text url apapun).
    """
    try:
        if url_contains_partial_text: # Periksa apakah string tidak kosong
            WebDriverWait(driver, timeout).until(
                EC.url_contains(url_contains_partial_text)
            )
        else: # Jika string kosong/tdk diinput argumentnya, tunggu sampai URL ada textnya apapun itu
             WebDriverWait(driver, timeout).until(EC.url_contains(""))

        actual_url = driver.current_url
        return actual_url

    except TimeoutException:
        logging.error(f"Timeout saat menunggu URL yang mengandung '{url_contains_partial_text}' setelah {timeout} detik")
        return None