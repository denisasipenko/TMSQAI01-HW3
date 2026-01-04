import pytest
import allure
from pages.login_page import LoginPage

# --- Test Data ---
VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"
ITEM_1 = "Sauce Labs Backpack"
ITEM_2 = "Sauce Labs Bike Light"
CHECKOUT_INFO = {
    "first_name": "John",
    "last_name": "Doe",
    "postal_code": "12345"
}


@pytest.mark.positive
@allure.epic("E-commerce Functionality")
@allure.feature("Login")
@allure.story("Successful Login")
class TestPositiveScenarios:

    @allure.title("Test Successful Login")
    @allure.description("Verify that a user can log in with valid credentials.")
    def test_successful_login(self, driver):
        """
        Tests successful login with valid credentials.
        """
        login_page = LoginPage(driver).open()
        inventory_page = login_page.login(VALID_USER, VALID_PASSWORD)
        assert inventory_page.get_title() == "Products", "Failed to log in successfully."

    @allure.title("Test Add Single Item to Cart")
    @allure.description("Verify that a user can add a single item to the shopping cart.")
    def test_add_single_item_to_cart(self, driver):
        """
        Tests adding a single item to the cart.
        """
        login_page = LoginPage(driver).open()
        inventory_page = login_page.login(VALID_USER, VALID_PASSWORD)
        inventory_page.add_item_to_cart(ITEM_1)
        assert inventory_page.get_cart_badge_item_count() == 1, "Cart badge count is not 1."
        cart_page = inventory_page.go_to_cart()
        assert cart_page.get_cart_items_count() == 1, "Item was not added to the cart."

    @allure.title("Test Add Multiple Items to Cart")
    @allure.description("Verify that a user can add multiple items to the shopping cart.")
    def test_add_multiple_items_to_cart(self, driver):
        """
        Tests adding multiple items to the cart.
        """
        login_page = LoginPage(driver).open()
        inventory_page = login_page.login(VALID_USER, VALID_PASSWORD)
        inventory_page.add_item_to_cart(ITEM_1)
        inventory_page.add_item_to_cart(ITEM_2)
        assert inventory_page.get_cart_badge_item_count() == 2, "Cart badge count is not 2."
        cart_page = inventory_page.go_to_cart()
        assert cart_page.get_cart_items_count() == 2, "Not all items were added to the cart."

    @allure.title("Test Remove Item from Cart")
    @allure.description("Verify that a user can remove an item from the shopping cart.")
    def test_remove_item_from_cart(self, driver):
        """
        Tests removing an item from the cart.
        """
        login_page = LoginPage(driver).open()
        inventory_page = login_page.login(VALID_USER, VALID_PASSWORD)
        inventory_page.add_item_to_cart(ITEM_1)
        assert inventory_page.get_cart_badge_item_count() == 1, "Precondition failed: Item not added."

        cart_page = inventory_page.go_to_cart()
        cart_page.remove_item(ITEM_1)
        assert cart_page.get_cart_items_count() == 0, "Item was not removed from the cart."

    @allure.title("Test Successful Checkout")
    @allure.description("Verify that a user can complete the checkout process successfully.")
    def test_successful_checkout(self, driver):
        """
        Tests the full, successful checkout process.
        """
        # 1. Login and add item
        login_page = LoginPage(driver).open()
        inventory_page = login_page.login(VALID_USER, VALID_PASSWORD)
        inventory_page.add_item_to_cart(ITEM_1)

        # 2. Go to cart and checkout
        cart_page = inventory_page.go_to_cart()
        checkout_step_one = cart_page.go_to_checkout()

        # 3. Fill info and continue
        checkout_step_one.fill_information(
            CHECKOUT_INFO["first_name"],
            CHECKOUT_INFO["last_name"],
            CHECKOUT_INFO["postal_code"]
        )
        checkout_step_two = checkout_step_one.continue_to_step_two()
        assert checkout_step_two.get_title() == "Checkout: Overview", "Failed to proceed to checkout overview."

        # 4. Finish checkout
        checkout_complete = checkout_step_two.click_finish()
        assert checkout_complete.get_title() == "Checkout: Complete!", "Checkout was not completed."
        assert checkout_complete.get_complete_header_text() == "Thank you for your order!", "Final confirmation message is incorrect."
