import os
import platform
import subprocess
import time
from datetime import datetime
from platform import python_version, system
from pytest_html import extras as pytest_html_extras
from datetime import datetime, timedelta, timezone
import pytest
from py.xml import html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from dataconfig.testdata import TestData as TD

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

# ---- capture error/failed testcase in report (khusus running di pipeline github menampilkan screenshot link) ----------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Capture the result of the test execution
    outcome = yield
    report = outcome.get_result()

    # Only capture screenshot on test failure
    if report.when == 'call' and report.outcome == 'failed':
        driver = getattr(item.instance, 'web_driver', None)  # Get driver instance

        if driver is not None:  # Ensure driver exists
            # Make sure the screenshots folder exists
            screenshot_dir = 'screenshots'
            os.makedirs(screenshot_dir, exist_ok=True)

            # Adjusting UTC to UTC+7
            local_time = datetime.now(timezone.utc) + timedelta(hours=7)
            timestamp = local_time.strftime("%Y%m%d_%H%M%S")

            # Path to save the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{item.name}_{timestamp}.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

            # Capture screenshot as base64
            screenshot_base64 = driver.get_screenshot_as_base64()

            # Attach screenshot to pytest-html report
            pytest_html = item.config.pluginmanager.getplugin('html')
            if pytest_html:
                extra = getattr(report, 'extra', [])
                extra.append(pytest_html.extras.image(screenshot_base64, title='Screenshot'))
                report.extra = extra

@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells):
    cells.pop()  # Hapus kolom terakhir ("Link") pada template laporan
    cells.insert(3, html.th("Screenshot"))  # Menambahkan kolom baru pada laporan dengan header name "Screenshot")


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
    if report.when == 'call' and report.failed:
        # Buat hyperlink ke kolom Screenshot dalam laporan
        run_id = os.getenv("GITHUB_RUN_ID")
        artifact_id = os.getenv("ARTIFACT_ID")
        screenshot_url = f"https://github.com/{os.getenv('GITHUB_REPOSITORY')}/actions/runs/{run_id}/artifacts/{artifact_id}"
        link = html.a("link here", href=screenshot_url, target="_blank")
        cells.insert(3, html.td(link))
        cells.pop()

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