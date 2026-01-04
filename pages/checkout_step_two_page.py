from selenium.webdriver.common.by import By
from utils.base_page import BasePage
from utils.logger import get_logger
import allure

logger = get_logger(__name__)


class CheckoutStepTwoPage(BasePage):
    """
    Page Object for the checkout overview page (Step Two).
    """
    # Locators
    FINISH_BUTTON = (By.ID, "finish")
    PAGE_TITLE = (By.CLASS_NAME, "title")

    @allure.step("Get page title")
    def get_title(self) -> str:
        """
        Gets the title of the checkout overview page.
        """
        logger.info("Getting checkout step two page title")
        title = self.get_text(*self.PAGE_TITLE)
        logger.info(f"Checkout step two page title is: '{title}'")
        return title

    @allure.step("Finish the checkout process")
    def click_finish(self):
        """
        Clicks the 'Finish' button to complete the purchase.
        """
        logger.info("Clicking finish button to complete checkout")
        self.js_click(*self.FINISH_BUTTON)
        logger.info("Clicked finish button")
        # This action leads to the final confirmation page
        from pages.checkout_complete_page import CheckoutCompletePage
        return CheckoutCompletePage(self.driver)
