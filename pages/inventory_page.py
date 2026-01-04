from selenium.webdriver.common.by import By
from utils.base_page import BasePage
from utils.logger import get_logger
import allure
from selenium.webdriver.support import expected_conditions as EC
from pages.cart_page import CartPage

logger = get_logger(__name__)


class InventoryPage(BasePage):
    """
    Page Object for the inventory/products page.
    """
    # Locators
    PAGE_TITLE = (By.CSS_SELECTOR, ".header_container .title")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    SHOPPING_CART_ICON = (By.CLASS_NAME, "shopping_cart_link")

    @allure.step("Get page title")
    def get_title(self) -> str:
        """
        Gets the title of the inventory page.
        """
        logger.info("Getting inventory page title")
        title = self.get_text(*self.PAGE_TITLE)
        logger.info(f"Inventory page title is: '{title}'")
        return title

    def get_add_to_cart_button_for_item(self, item_name: str):
        """Returns the locator for the 'Add to cart' button of a specific item."""
        return (By.XPATH, f"//div[text()='{item_name}']/ancestor::div[contains(@class, 'inventory_item')]//button[text()='Add to cart']")

    def get_remove_button_for_item(self, item_name: str):
        """Returns the locator for the 'Remove' button of a specific item."""
        return (By.XPATH, f"//div[text()='{item_name}']/ancestor::div[contains(@class, 'inventory_item')]//button[text()='Remove']")

    @allure.step("Add item '{item_name}' to cart")
    def add_item_to_cart(self, item_name: str):
        """
        Clicks the 'Add to cart' button for a specific item and waits for it to change to 'Remove'.
        """
        logger.info(f"Adding item '{item_name}' to cart")
        add_button_locator = (By.XPATH, f"//div[text()='{item_name}']/ancestor::div[contains(@class, 'inventory_item')]//button[text()='Add to cart']")
        self.js_click(*add_button_locator)
        logger.info(f"Clicked 'Add to cart' for item '{item_name}'")

        # Wait for the button to change to 'Remove'
        remove_button_locator = self.get_remove_button_for_item(item_name) # This uses the specific item name to find its remove button
        self.wait.until(EC.visibility_of_element_located(remove_button_locator))
        logger.info(f"Verified '{item_name}' is added (Remove button visible).")
        return self

    @allure.step("Remove item '{item_name}' from cart")
    def remove_item_from_cart(self, item_name: str):
        """
        Clicks the 'Remove' button for a specific item from the inventory page.
        """
        logger.info(f"Removing item '{item_name}' from cart")
        button_locator = self.get_remove_button_for_item(item_name)
        self.click(*button_locator)
        logger.info(f"Clicked 'Remove' for item '{item_name}'")
        return self

    @allure.step("Go to the shopping cart")
    def go_to_cart(self):
        """
        Clicks the shopping cart icon to navigate to the cart page.
        """
        logger.info("Navigating to the shopping cart")
        self.js_click(*self.SHOPPING_CART_ICON)
        logger.info("Clicked shopping cart icon")
        
        # Explicitly wait for the URL to change to the cart page
        self.wait.until(EC.url_to_be("https://www.saucedemo.com/cart.html"))
        logger.info("Navigated to cart page.")
        return CartPage(self.driver)

    @allure.step("Get number of items in the cart icon")
    def get_cart_badge_item_count(self) -> int:
        """
        Gets the number displayed on the shopping cart badge. Returns 0 if empty.
        """
        logger.info("Getting cart badge item count")
        try:
            badge = self.find_element(By.CLASS_NAME, "shopping_cart_badge")
            count = int(badge.text)
            logger.info(f"Cart badge count is {count}")
            return count
        except Exception:
            logger.info("Cart badge is not displayed (cart is likely empty)")
            return 0
