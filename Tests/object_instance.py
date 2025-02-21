from pages.aboutpage import AboutPageAction
from pages.cartpage import CartPageAction
from pages.loginpage import LoginPageAction
from pages.productspage import ProductsPageAction


class ObjectInstances:

    def loginpage(self):
        return LoginPageAction(self.driver)

    def productpage(self):
        return ProductsPageAction(self.driver)

    def aboutpage(self):
        return AboutPageAction(self.driver)

    def cartpage(self):
        return CartPageAction(self.driver)