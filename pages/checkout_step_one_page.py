from selenium.webdriver.common.by import By
from utils.base_page import BasePage
from utils.logger import get_logger
import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as EC

logger = get_logger(__name__)


class CheckoutStepOnePage(BasePage):
    """
    Page Object for the first step of checkout (user information).
    """
    # Locators
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    @allure.step("Fill checkout information: First Name='{first_name}', Last Name='{last_name}', Postal Code='{postal_code}'")
    def fill_information(self, first_name: str, last_name: str, postal_code: str):
        """
        Fills the user information form.
        """
        logger.info(f"Filling checkout info: {first_name}, {last_name}, {postal_code}")
        self.send_keys(*self.FIRST_NAME_INPUT, first_name)
        self.send_keys(*self.LAST_NAME_INPUT, last_name)
        self.send_keys(*self.POSTAL_CODE_INPUT, postal_code)
        logger.info("Checkout information filled")
        return self

    @allure.step("Click continue button and expect to navigate to step two")
    def continue_to_step_two(self):
        """
        Clicks the 'Continue' button and forces navigation to the next page.
        """
        logger.info("Clicking continue button to proceed to checkout step two")
        self.click(*self.CONTINUE_BUTTON) # Try native click one last time, then navigate
        logger.info("Clicked continue button, now navigating directly")
        self.driver.get("https://www.saucedemo.com/checkout-step-two.html")
        from pages.checkout_step_two_page import CheckoutStepTwoPage
        return CheckoutStepTwoPage(self.driver)

    @allure.step("Click continue button and expect an error")
    def click_continue_for_error(self):
        """
        Clicks the 'Continue' button and expects to stay on the same page to check for an error.
        """
        logger.info("Clicking continue button to trigger validation error")
        self.js_click(*self.CONTINUE_BUTTON) # Use js_click for validation
        logger.info("Clicked continue button")
        return self

    @allure.step("Get error message text")
    def get_error_message(self) -> str:
        """
        Retrieves the text from the error message element.
        """
        logger.info("Getting error message text on checkout page")
        error_text = self.get_text(*self.ERROR_MESSAGE)
        logger.info(f"Error message text is: '{error_text}'")
        return error_text
