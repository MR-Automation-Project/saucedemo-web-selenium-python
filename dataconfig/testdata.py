class BaseURL:
    DEV = ""
    TESTING = "https://saucedemo.com"
    STAGING = ""
    PROD = ""

class UserAccount:
    STANDARD_USER = "standard_user"
    LOCKED_USER = "locked_out_user"
    VISUAL_USER = "visual_user"
    GLITCH_USER = "performance_glitch_user"
    GENERAL_PASSWORD = "secret_sauce"

    #for parametrize some credential user:
    valid_users = [
        {"username": "standard_user", "password": "secret_sauce"},
        {"username": "visual_user", "password": "secret_sauce"}
    ]

class ProductItems:

    #sample for parametrize in scenario add to cart more than 1 items
    products_name = [
        {"nama_produk1": "Sauce Labs Bike Light",
         "nama_produk2": "Sauce Labs Fleece Jacket",
         "nama_produk3": "Sauce Labs Backpack"}
    ]