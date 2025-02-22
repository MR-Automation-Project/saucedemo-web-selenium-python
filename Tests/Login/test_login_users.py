import time

import pytest

from Tests.conftest import class_scope
from dataconfig.testdata import UserAccount as UA
from utils import refresh_browser, take_screenshot
from Tests.object_instance import ObjectInstances

@pytest.mark.usefixtures("setup_scope_function")
class TestValidLogin(ObjectInstances):
    @pytest.mark.parametrize("akun", UA.valid_users)
    def test_login_with_valid_account(self, akun):
        self.loginpage().login(akun['username'], akun['password'])
        assert self.productpage().check_visibility_page_title_on_products_page(), "gagal landing on product page"

@pytest.mark.usefixtures("setup_scope_class")
class TestInvalidLogin(ObjectInstances):

    def test_login_with_blank_all_field(self):
        self.loginpage().click_login_button()
        error_msg = self.loginpage().get_error_message()
        assert error_msg == "Epic sadface: Username is required", \
            f"Unexpected error message did not match. Actual Found is: {error_msg}"

    def test_login_with_empty_password_field(self):
        self.loginpage().input_username_field(UA.STANDARD_USER)
        self.loginpage().click_login_button()
        error_msg = self.loginpage().get_error_message()
        assert error_msg == "Epic sadface: Password is required", \
            f"Unexpected error message did not match. Actual Found is: {error_msg}"

    def test_login_with_empty_user_field(self):
        refresh_browser(self.driver)
        self.loginpage().input_password_field(UA.GENERAL_PASSWORD)
        self.loginpage().click_login_button()
        error_msg = self.loginpage().get_error_message()
        assert error_msg == "Epic sadface: Username is required", \
            f"Unexpected error message did not match. Actual Found is: {error_msg}"
        take_screenshot(self.driver, "ss_test")

    def test_login_with_locked_user_account(self):
        refresh_browser(self.driver)
        self.loginpage().input_username_field(UA.LOCKED_USER)
        self.loginpage().input_password_field(UA.GENERAL_PASSWORD)
        self.loginpage().click_login_button()
        error_msg = self.loginpage().get_error_message()
        assert error_msg == "Epic sadface: Sorry, this user has been locked out.", \
            f"Unexpected error message did not match. Actual Found is: {error_msg}"