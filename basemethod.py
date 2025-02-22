"""
    basemethod.py : action method yang bisa dilakukan pada halaman(page object)
                        digunakan pada layer pages
"""
import logging
import os
import time
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import *

class Basemethod:

    def __init__(self, driver):
        self.driver = driver

    def _click_on(self, locator):
        try:
            if isinstance(locator, tuple):
                wait_for_element_to_be_visible(self.driver, locator).click()
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
        element = wait_for_element_to_be_visible(self.driver, locator)
        element.clear()
        element.send_keys(input_text)

    def _clear_on_textbox(self, locator):
        wait_for_element_to_be_visible(self.driver, locator).clear()

    def _is_element_visible(self, locator):
        return bool(wait_for_element_to_be_visible(self.driver, locator))

    def _get_text_element(self, locator):
        return wait_for_element_to_be_visible(self.driver, locator).text

    def _get_attribute_element(self, locator, attribute):
        return wait_for_element_to_be_visible(self.driver, locator).get_attribute(attribute)

    def _drag_and_drop(self, source_locator, target_locator):
        source = wait_for_element_to_be_visible(self.driver, source_locator)
        target = wait_for_element_to_be_visible(self.driver, target_locator)
        action = ActionChains(self.driver).drag_and_drop(source, target)
        action.perform()

    def _switch_to_frame(self, locator):
        wait_for_frame_to_be_avail_and_switch_to_it(self.driver, locator)

    def _switch_to_default_frame(self):
        self.driver.switch_to.default_content()

    def _get_length_all_elements(self, locator):
        return len(wait_for_element_to_be_visible(self.driver, locator))

    def _hover_over_element(self, locator):
        target_element = wait_for_element_to_be_visible(self.driver, locator)
        actions = ActionChains(self.driver).move_to_element(target_element)
        actions.perform()

    def _capture_evidence(self, name):
        # Make sure the folder exists in the root of project directory,
        # jika tidak maka buat folder "screenshots"
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        #Tentukan path dan nama file+formatnya utk wadah screenshot
        screenshot_path = os.path.join(screenshot_dir, f"{name}.png")
        self.driver.save_screenshot(screenshot_path)

    """-----------------------Handling DROPDOWN AREA - Select and non-select---------------------------"""

    def _select_dropdown_by_index(self, locator, index, timeout=10):
        """Memilih option list dalam dropdown berdasarkan index.
        Args:
            locator: Tuple berisi jenis locator dan nilai locator (misal: ("id", "dropdown_id")).
            index: Index opsi yang akan dipilih (mulai dari 0).
            timeout: default Waktu tunggu maksimum dalam detik.
        """
        try:
            element = wait_for_element_to_be_presence(self.driver, locator)
            select = Select(element) #Buat object select
            select.select_by_index(index)
            logging.info(f"Opsi dropdown dengan index {index} berhasil dipilih.")
        except TimeoutException:
            logging.error(f"Timeout saat menunggu dropdown muncul setelah {timeout} detik.")
            return None
        except Exception as e: # Tangani exception umum untuk berjaga-jaga
            logging.error(f"Terjadi kesalahan saat memilih dropdown: {e}")
            return None

    def _select_dropdown_by_value(self, locator, value, timeout=10):
        """Memilih option list dalam dropdown berdasarkan value.
        Args:
            locator: Tuple berisi jenis locator dan nilai locator (misal: ("id", "dropdown_id")).
            value: Value dari opsi yang akan dipilih.
            timeout: Waktu tunggu maksimum dalam detik.
        """
        try:
            element = wait_for_element_to_be_presence(self.driver, locator)
            select = Select(element)  # Buat objek Select
            select.select_by_value(value)
            logging.info(f"Opsi dropdown dengan value '{value}' berhasil dipilih.")
        except TimeoutException:
            logging.error(f"Timeout saat menunggu dropdown muncul setelah {timeout} detik.")
            return None
        except Exception as e:  # Tangani exception umum untuk berjaga-jaga
            logging.error(f"Terjadi kesalahan saat memilih dropdown: {e}")
            return None

    def _select_dropdown_by_visible_text(self, locator, text, timeout=10):
        """Memilih opsi dropdown berdasarkan teks yang terlihat.
        Args:
            locator: Tuple berisi jenis locator dan nilai locator.
            text: Teks yang terlihat pada opsi yang akan dipilih.
            timeout: Waktu tunggu maksimum dalam detik.
        """
        try:
            element = wait_for_element_to_be_presence(self.driver, locator)
            select = Select(element)
            select.select_by_visible_text(text)
            logging.info(f"Opsi dropdown dengan teks '{text}' berhasil dipilih.")
        except TimeoutException:
            logging.error(f"Timeout saat menunggu dropdown muncul setelah {timeout} detik.")
            return None
        except NoSuchElementException:
            logging.error(f"Opsi dropdown dengan teks '{text}' tidak ditemukan.")
            return None
        except Exception as e:
            logging.error(f"Terjadi kesalahan saat memilih dropdown: {e}")
            return None

    def _select_dropdown_by_text_partial(self, locator, partial_text, timeout=10):
        """Memilih opsi dropdown berdasarkan sebagian teks yang terlihat.
           Berguna untuk dropdown yang tidak memiliki value yang unik.
        Args:
            locator: Tuple berisi jenis locator dan nilai locator.
            partial_text: Sebagian teks yang terlihat pada opsi.
            timeout: Waktu tunggu maksimum dalam detik.
        """
        try:
            element = wait_for_element_to_be_presence(self.driver, locator)

            options = element.find_elements("tag name", "option")  # ambil semua option (multi elementss)
            for option in options:
                if partial_text in option.text:
                    option.click()
                    logging.info(f"Opsi dropdown dengan sebagian teks '{partial_text}' berhasil dipilih.")
                    return True

            logging.error(f"Opsi dropdown dengan sebagian teks '{partial_text}' tidak ditemukan.")
            return None

        except TimeoutException:
            logging.error(f"Timeout saat menunggu dropdown muncul setelah {timeout} detik.")
            return None
        except Exception as e:
            logging.error(f"Terjadi kesalahan saat memilih dropdown: {e}")
            return None

    def _find_option_in_dropdown(self, dropdown_element, search_strategy, search_value, timeout=10):
        """Mencari elemen opsi dropdown berdasarkan strategi dan nilai pencarian.
        Args:
            dropdown_element: WebElement dari dropdown yang sudah dibuka.
            search_strategy: Strategi pencarian (misalnya "text", "attribute", dll.).
            search_value: Nilai yang dicari.
            timeout: Waktu tunggu maksimum dalam detik.

        Returns:
            WebElement: Jika opsi ditemukan, mengembalikan WebElement dari opsi tersebut.
            None: Jika opsi tidak ditemukan.
        """
        try:
            if search_strategy == "text":
                options = dropdown_element.find_elements("xpath", ".//*")  # Cari semua elemen di dalam dropdown
                for option in options:
                    if option.text == search_value:
                        return option
            elif search_strategy == "attribute":
                # Contoh: Mencari berdasarkan atribut 'data-value'
                option_element = dropdown_element.find_element("xpath", f".//*[@data-value='{search_value}']")
                return option_element
            # ... tambahkan strategi pencarian lain sesuai kebutuhan ...
            return None  # jika tidak ada yang cocok

        except TimeoutException:
            logging.error(f"Timeout saat mencari opsi '{search_value}' di dalam dropdown.")
            return None
        except Exception as e:
            logging.error(f"Terjadi kesalahan saat mencari opsi di dalam dropdown: {e}")
            return None

    def _handle_non_standard_dropdown(self, dropdown_locator, search_strategy, search_value, timeout=10):
        """Menangani dropdown non-standar.
        Args:
            dropdown_locator: Tuple berisi jenis locator dan nilai locator untuk dropdown.
            search_strategy: Strategi pencarian (misalnya "text", "attribute").
            search_value: Nilai yang dicari.
            timeout: Waktu tunggu maksimum dalam detik.
        """
        try:
            dropdown_element = wait_for_element_to_be_clickable(self.driver, dropdown_locator)
            dropdown_element.click()  # Buka dropdown
            option_element = self._find_option_in_dropdown(dropdown_element, search_strategy, search_value)

            if option_element:
                option_element.click()
                logging.info(f"Opsi dropdown non-standar dengan {search_strategy} '{search_value}' berhasil dipilih.")
                return True
            else:
                logging.error(f"Opsi dengan {search_strategy} '{search_value}' tidak ditemukan di dalam dropdown.")
                return None

        except TimeoutException:
            logging.error(f"Timeout saat menunggu dropdown muncul setelah {timeout} detik.")
            return None
        except Exception as e:
            logging.error(f"Terjadi kesalahan saat menangani dropdown non-standar: {e}")
            return None