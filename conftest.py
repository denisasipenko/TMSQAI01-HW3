import os
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime


@pytest.fixture(scope="function")
def driver():
    """
    Pytest fixture to initialize and quit WebDriver for each test function.
    """
    chrome_options = ChromeOptions()
    chrome_options.add_experimental_option(
        "prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False}
    )

    base_driver_path = ChromeDriverManager().install()
    # Correct the path if it points to THIRD_PARTY_NOTICES.chromedriver
    if "THIRD_PARTY_NOTICES.chromedriver" in base_driver_path:
        driver_dir = os.path.dirname(base_driver_path)
        driver_executable_path = os.path.join(driver_dir, "chromedriver")
    else:
        driver_executable_path = base_driver_path

    print(f"DEBUG: Using driver executable path: {driver_executable_path}")
    service = ChromeService(executable_path=driver_executable_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)  # Implicit wait
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to take screenshot on test failure and attach to Allure report.
    """
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        try:
            # Access the 'driver' fixture from the test item
            driver_instance = item.funcargs['driver']
            # Create a unique name for the screenshot
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            screenshot_name = f"failed_test_{item.name}_{timestamp}.png"
            # Take screenshot and attach to Allure
            allure.attach(
                driver_instance.get_screenshot_as_png(),
                name=screenshot_name,
                attachment_type=AttachmentType.PNG
            )
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
