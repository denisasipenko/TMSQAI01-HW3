import pytest
import allure
from pages.login_page import LoginPage

# --- Test Data ---
VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"
ITEM_1 = "Sauce Labs Backpack"


@pytest.mark.validation
@allure.epic("E-commerce Functionality")
@allure.feature("Checkout")
@allure.story("Field Validation")
class TestValidationScenarios:

    @allure.title("Test Checkout with Missing Information")
    @allure.description("Verify that an error is shown when trying to checkout without filling required fields.")
    def test_checkout_with_missing_info(self, driver):
        """
        Tests that an error message appears if checkout is attempted without filling in the user info.
        """
        # 1. Login and add an item to the cart
        login_page = LoginPage(driver).open()
        inventory_page = login_page.login(VALID_USER, VALID_PASSWORD)
        inventory_page.add_item_to_cart(ITEM_1)

        # 2. Proceed to checkout info page
        cart_page = inventory_page.go_to_cart()
        checkout_page = cart_page.go_to_checkout()

        # 3. Click 'Continue' without filling fields
        checkout_page.click_continue_for_error()

        # 4. Verify error message
        expected_error = "Error: First Name is required"
        actual_error = checkout_page.get_error_message()

        assert actual_error == expected_error, "The error message for missing first name is incorrect."
        assert "checkout-step-two.html" not in checkout_page.get_current_url(), "User was incorrectly advanced to the next checkout step."
