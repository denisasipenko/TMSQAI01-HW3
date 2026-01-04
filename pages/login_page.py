from selenium.webdriver.common.by import By
from pages.inventory_page import InventoryPage
from utils.base_page import BasePage
from utils.logger import get_logger
import allure

logger = get_logger(__name__)


class LoginPage(BasePage):
    """
    Page Object for the Sauce Demo login page.
    """
    URL = "https://www.saucedemo.com/"

    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    @allure.step("Open the login page")
    def open(self):
        """
        Navigates to the login page URL.
        """
        logger.info("Opening login page")
        self.driver.get(self.URL)
        logger.info("Login page opened")
        return self

    @allure.step("Log in with username: '{username}' and password: '{password}'")
    def login(self, username, password) -> InventoryPage:
        """
        Fills the login form and submits it.
        """
        logger.info(f"Attempting to log in with username: {username}")
        self.send_keys(*self.USERNAME_INPUT, username)
        self.send_keys(*self.PASSWORD_INPUT, password)
        self.click(*self.LOGIN_BUTTON)
        logger.info("Login form submitted")
        return InventoryPage(self.driver)

    @allure.step("Get error message text")
    def get_error_message(self) -> str:
        """
        Retrieves the text from the error message element.
        """
        logger.info("Getting error message text")
        error_text = self.get_text(*self.ERROR_MESSAGE)
        logger.info(f"Error message text is: '{error_text}'")
        return error_text
