import pytest
import allure
from pages.login_page import LoginPage

# --- Test Data ---
VALID_USER = "standard_user"
INVALID_PASSWORD = "wrong_password"


@pytest.mark.negative
@allure.epic("E-commerce Functionality")
@allure.feature("Login")
@allure.story("Failed Login")
class TestNegativeScenarios:

    @allure.title("Test Login with Invalid Password")
    @allure.description("Verify that an error message is shown for login with an incorrect password.")
    def test_login_with_invalid_password(self, driver):
        """
        Tests that login fails with an incorrect password and an error message is displayed.
        """
        login_page = LoginPage(driver).open()
        login_page.login(VALID_USER, INVALID_PASSWORD)

        expected_error = "Epic sadface: Username and password do not match any user in this service"
        actual_error = login_page.get_error_message()

        assert actual_error == expected_error, "Error message for invalid login is incorrect."
        assert "inventory.html" not in login_page.get_current_url(), "User was redirected to inventory despite invalid login."
