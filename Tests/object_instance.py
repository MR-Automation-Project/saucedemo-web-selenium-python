from pages.aboutpage import AboutPageAction
from pages.cartpage import CartPageAction
from pages.loginpage import LoginPageAction
from pages.productspage import ProductsPageAction


class ObjectInstances:

    def loginpage(self):
        obj = LoginPageAction(self.driver)
        return obj

    def productpage(self):
        obj = ProductsPageAction(self.driver)
        return obj

    def aboutpage(self):
        obj = AboutPageAction(self.driver)
        return obj

    def cartpage(self):
        obj = CartPageAction(self.driver)
        return obj