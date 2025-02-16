import os
import time
import pytest
import platform
from platform import python_version, system
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from dataconfig.testdata import TestData as TD
import subprocess


'''------------------------------ Setup Hook for Report -------------------------------------'''
def pytest_html_report_title(report):
    report.title = "["+report.config.getoption("--url") + " env] "+"Automation Testing Report of WEB Sauce Demo"

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


'''--------------------------------- Add options for running pytest -------------------------------'''
def pytest_addoption(parser):
    # can be run in terminal like this : pytest -vs --browser=chrome,firefox (default firefox if not defined)
    parser.addoption("--browser", action="append", default=[])
    parser.addoption("--url", action="store", default="testing")


'''------------Parameterisasi test scr dinamis : memungkinkan jalan di beberapa browser------'''
def pytest_generate_tests(metafunc):
    if 'browser' in metafunc.fixturenames:
        browsers = metafunc.config.getoption("browser")
        metafunc.parametrize("browser", browsers)

'''---------------------------------Fixture Scope : Per TEST FUNCTION / METHOD ---------------------------------'''
@pytest.fixture(scope="function")
def setup_scope_function(request, browser):
    url = request.config.getoption("url")
    web_driver = None

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # for chrome only
        options.add_experimental_option("detach", True)
        options.add_argument("--disable-notifications")  # for chrome only
        options.add_argument("--start-maximized")
        options.add_argument('--log-level=3')
        #options.add_argument('--headless')
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

    if url == "testing":
        web_driver.get(TD.BASE_URL_TEST)
    elif url == "staging":
        web_driver.get(TD.BASE_URL_STAG)
    elif url == "prod":
        web_driver.get(TD.BASE_URL_PROD)

    request.cls.driver = web_driver
    yield
    time.sleep(1.5)
    web_driver.quit()

    # capture screenshot jika ada test failed
SCREENSHOT_DIR = "screenshots"
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"{item.name}_{timestamp}.png"
        screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)

        # Pastikan direktori screenshot ada
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)

        try:
            if hasattr(item.instance, 'driver'):  # check driver exist to avoid exception when browser not launch
                item.instance.driver.save_screenshot(screenshot_path)
                # Sisipkan path screenshot ke dalam laporan HTML
                report.extra_html = f'<img src="{screenshot_path}" alt="screenshot" width="400" height="300"/>'
            else:
                print("Driver tidak tersedia untuk mengambil screenshot.")
        except Exception as e:
            print(f"Gagal mengambil screenshot: {e}")