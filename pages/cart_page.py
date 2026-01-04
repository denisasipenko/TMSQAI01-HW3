from selenium.webdriver.common.by import By
from utils.base_page import BasePage
from utils.logger import get_logger
import allure
from selenium.webdriver.support import expected_conditions as EC

logger = get_logger(__name__)


class CartPage(BasePage):
    """
    Page Object for the shopping cart page.
    """
    # Locators
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def get_remove_button_for_item(self, item_name: str):
        """Returns the locator for the 'Remove' button of a specific item in the cart."""
        # Convert item name to a slug format, e.g., "Sauce Labs Backpack" -> "remove-sauce-labs-backpack"
        data_test_value = f"remove-{item_name.lower().replace(' ', '-')}"
        return (By.CSS_SELECTOR, f"[data-test='{data_test_value}']")

    @allure.step("Get the number of items in the cart")
    def get_cart_items_count(self) -> int:
        """
        Counts the number of items listed in the cart.
        """
        logger.info("Getting number of items in the cart")
        try:
            items = self.find_elements(*self.CART_ITEMS)
            count = len(items)
            logger.info(f"Found {count} items in the cart")
            return count
        except Exception:
            logger.info("No items found in the cart")
            return 0

    @allure.step("Remove item '{item_name}' from the cart")
    def remove_item(self, item_name: str):
        """
        Clicks the 'Remove' button for a specific item in the cart.
        """
        logger.info(f"Removing item '{item_name}' from the cart")
        button_locator = self.get_remove_button_for_item(item_name)
        self.js_click(*button_locator)
        logger.info(f"Clicked 'Remove' for item '{item_name}'")
        return self

    @allure.step("Proceed to checkout")
    def go_to_checkout(self):
        """
        Clicks the checkout button.
        """
        logger.info("Proceeding to checkout")
        self.js_click(*self.CHECKOUT_BUTTON)
        logger.info("Clicked checkout button")
        from pages.checkout_step_one_page import CheckoutStepOnePage
        return CheckoutStepOnePage(self.driver)
