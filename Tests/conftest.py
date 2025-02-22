import os
import time
import pytest
import platform
from platform import python_version, system

from pytest_html import extras
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from dataconfig.testdata import BaseURL
import subprocess

SCREENSHOT_DIR = "screenshots"

#------------- Setup Pytest Hook : adjust Report Title ---------#
def pytest_html_report_title(report):
    report.title = "["+report.config.getoption("--url") + " env] "+"Automation Testing Report of WEB Sauce Demo"

#------------- Setup Pytest Hook : adjust Metadata info for Report ---------#
@pytest.hookimpl(tryfirst=True)
def pytest_metadata(metadata, config):
    keys_to_remove = ['Python', 'Platform', 'Packages', 'JAVA_HOME', 'Plugins']
    for key in keys_to_remove:
        if key in metadata:
            del metadata[key]

    metadata['Python Ver.'] = python_version()
    metadata['Pytest Framework Ver.'] = pytest.__version__
    metadata['Platform OS'] = "{} {} {} {}".format(system(), platform.release(), platform.version(), platform.machine())
    # Menambahkan informasi browser ke metadata
    browser = config.getoption("--browser")
    if browser:
        metadata['Browser'] = ', '.join(browser)


# ------------- Add options for running pytest --------------#
def pytest_addoption(parser):
    # can be run in terminal like this : pytest -vs --browser=chrome,firefox (default firefox if not defined)
    parser.addoption("--browser", action="append", default=[])
    parser.addoption("--url", action="store", default="testing")

def pytest_configure(config):
    config.addinivalue_line("markers", "class_scope: marks tests that use class-level scope for browser parameterization")

# Marker untuk menandai test dengan scope "class"
@pytest.mark.class_scope  # Definisikan sebagai marker pytest
def class_scope():
    pass


# ----------Handling multiple scope in same test class --- #
def pytest_generate_tests(metafunc):
    if 'browser' in metafunc.fixturenames:
        browsers = metafunc.config.getoption("--browser")
        if not browsers:
            browsers = ["chrome"]  # Default browser

        # Parameterisasi untuk scope "class"
        if hasattr(metafunc.cls, "class_scope"):  # Periksa di level class
            metafunc.parametrize("browser", browsers, scope="class")
        # Parameterisasi untuk scope "function"
        else:
            metafunc.parametrize("browser", browsers, scope="function")

    """Changes 4"""
    # if 'browser' in metafunc.fixturenames:
    #     browsers = metafunc.config.getoption("--browser")
    #     if not browsers:
    #         browsers = ["chrome"]  # Default browser
    #
    #     # Parameterize di level function, tetapi scope class akan menangani instance class yang berbeda
    #     metafunc.parametrize("browser", browsers, scope="function")

    """Changes 3"""
    # if 'browser' in metafunc.fixturenames:
    #     browsers = metafunc.config.getoption("--browser")
    #     if not browsers:
    #         browsers = ["chrome"]  # Default browser
    #
    #     # Periksa apakah class memiliki marker "class_scope"
    #     if hasattr(metafunc.cls, "class_scope"):
    #         metafunc.parametrize("browser", browsers, scope="class")
    #     else:
    #         metafunc.parametrize("browser", browsers, scope="function")

"""CHanges 2"""
    # if 'browser' in metafunc.fixturenames:
    #     browsers = metafunc.config.getoption("--browser")
    #     if not browsers:
    #         browsers = ["chrome"]  # Default browser if none specified
    #
    #     # Perhatikan perubahan ini: scope sekarang "function"
    #     metafunc.parametrize("browser", browsers, scope="function")

"""changes 1"""
        # if 'browser' in metafunc.fixturenames:
    #     if metafunc.cls is None:  # Ini adalah test function (scope function)
    #         browser = metafunc.config.getoption("--browser") # Ambil browser dari command line
    #         metafunc.parametrize("browser", [browser]) # Parameterize dengan nilai tersebut
    #     else:  # Ini adalah test class (scope class)
    #         browser = metafunc.config.getoption("--browser")  # Ambil browser dari command line
    #         metafunc.parametrize("browser", [browser])  # Parameterize dengan nilai tersebut


# --------------Create web driver----------------- #
def create_web_driver(browser):
    web_driver = None

    if isinstance(browser, list):  # Periksa apakah browser berupa list
        browser = browser[0]  # Ambil elemen pertama dari list
    # Sekarang browser dipastikan string, bukan list lagi

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # for chrome only
        options.add_experimental_option("detach", True)
        options.add_argument("--disable-notifications")  # for chrome only
        options.add_argument("--start-maximized")
        options.add_argument('--log-level=3')
        # options.add_argument('--headless')
        web_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    elif browser == "edge":
        options = webdriver.EdgeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # for chrome only
        options.add_experimental_option("detach", True)
        options.add_argument("--disable-notifications")  # for chrome only
        options.add_argument("--start-maximized")
        options.add_argument('--log-level=3')
        # options.add_argument('--headless')
        web_driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')
        web_driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)


    elif browser == "safari":
        if platform.system() != "Darwin":
            pytest.fail("Safari hanya bisa dijalankan di macOS!")

        # Enable Safari WebDriver via CLI**
        try:
            subprocess.run(["sudo", "safaridriver", "--enable"], check=True)
        except Exception as e:
            pytest.fail(f"Error saat mengaktifkan Safari WebDriver: {e}")

        # Jalankan Safari WebDriver
        options = webdriver.SafariOptions()
        web_driver = webdriver.Safari(options=options)
    else:
        pytest.fail(f"Browser '{browser}' is not supported!")

    return web_driver

# ---------------Fixture Scope : Per TEST FUNCTION / METHOD ----------- #
@pytest.fixture(scope="function", autouse=True)
def setup_scope_function(request, browser):
    if hasattr(request.cls, "class_scope"):
        if request.cls.driver is None:  # Cek apakah driver sudah diinisialisasi
            web_driver = create_web_driver(browser)
            url = request.config.getoption("url")

            if url == "testing":
                web_driver.get(BaseURL.TESTING)
            elif url == "staging":
                web_driver.get(BaseURL.STAGING)
            elif url == "prod":
                web_driver.get(BaseURL.PROD)
            elif url == "dev":
                web_driver.get(BaseURL.DEV)
            else:
                pytest.fail(f"URL '{url}' is not valid!")
            request.cls.driver = web_driver # simpan driver yang diinisialisasi
        yield
        # Tidak perlu quit di sini, karena sudah dihandle oleh scope class
    else:
        web_driver = create_web_driver(browser)
        url = request.config.getoption("url")

        if url == "testing":
            web_driver.get(BaseURL.TESTING)
        elif url == "staging":
            web_driver.get(BaseURL.STAGING)
        elif url == "prod":
            web_driver.get(BaseURL.PROD)
        elif url == "dev":
            web_driver.get(BaseURL.DEV)
        else:
            pytest.fail(f"URL '{url}' is not valid!")

        request.cls.driver = web_driver
        yield
        time.sleep(1.5)
        web_driver.quit()


# ---------------Fixture Scope : Per CLASS ----------- #
@pytest.fixture(scope="class", autouse=True)
def setup_scope_class(request):
    request.cls.driver = None  # Placeholder
    yield

# -------handling screenshot jika ada failed pytest --------- #
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot if test fails and attach to pytest-html report."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"{item.name}_{timestamp}.png"
        screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)

        os.makedirs(SCREENSHOT_DIR, exist_ok=True)  # Pastikan direktori screenshot ada

        driver = getattr(item, 'driver', None)
        if driver:
            driver.save_screenshot(screenshot_path)
            if "pytest_html" in item.config.pluginmanager.list_plugin_names():
                extra = getattr(report, "extra", [])
                extra.append(extras.image(screenshot_path))
                report.extra = extra
        else:
            print("Driver tidak tersedia untuk mengambil screenshot.")