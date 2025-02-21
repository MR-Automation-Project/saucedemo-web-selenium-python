import pytest
from dataconfig.testdata import accounts
from Tests.object_instance import ObjectInstances


@pytest.mark.usefixtures("setup_scope_function")
class TestLoginAndNavigateAboutPage(ObjectInstances):

    @pytest.mark.debug
    @pytest.mark.parametrize("akun", accounts)
    def test_navigate_to_about_page(self, akun):
        # Automate login flow, click on hamburger button (top left), navigate to 'About' and verify if it successfully navigated or not.
        self.loginpage().login(akun['username'], akun['password'])
        self.productpage().navigate_to_about_via_hamburgermenu()
        assert self.aboutpage().check_visibility_subtext_in_aboutpage(), "failed to landing on about page"


