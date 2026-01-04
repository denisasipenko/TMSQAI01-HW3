from selenium.webdriver.common.by import By
from utils.base_page import BasePage
from utils.logger import get_logger
import allure

logger = get_logger(__name__)


class CheckoutCompletePage(BasePage):
    """
    Page Object for the final checkout confirmation page.
    """
    # Locators
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    PAGE_TITLE = (By.CLASS_NAME, "title")

    @allure.step("Get page title")
    def get_title(self) -> str:
        """
        Gets the title of the checkout complete page.
        """
        logger.info("Getting checkout complete page title")
        title = self.get_text(*self.PAGE_TITLE)
        logger.info(f"Checkout complete page title is: '{title}'")
        return title

    @allure.step("Get completion message header")
    def get_complete_header_text(self) -> str:
        """
        Gets the text from the main header on the confirmation page.
        """
        logger.info("Getting checkout completion header text")
        header_text = self.get_text(*self.COMPLETE_HEADER)
        logger.info(f"Completion header text is: '{header_text}'")
        return header_text
