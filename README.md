# UI Automation Test Project for Sauce Demo

This project contains UI automated tests for the Sauce Demo e-commerce website (https://www.saucedemo.com/). It is built using Python, Selenium, PyTest, and Allure for reporting.

## Project Structure

The project follows a standard Page Object Model (POM) structure to ensure scalability and maintainability.

```
/
├── pages/                 # Page Object classes for each page of the application
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   ├── checkout_step_one_page.py
│   ├── checkout_step_two_page.py
│   └── checkout_complete_page.py
├── tests/                 # Test scripts organized by type
│   ├── positive/
│   │   └── test_positive_scenarios.py
│   ├── negative/
│   │   └── test_negative_scenarios.py
│   └── validation/
│       └── test_validation_scenarios.py
├── utils/                 # Helper modules like logging
│   ├── base_page.py
│   └── logger.py
├── resources/             # Configuration files
│   └── allure.properties
├── conftest.py            # PyTest fixtures and hooks (e.g., WebDriver setup)
├── requirements.txt       # Project dependencies
└── README.md              # This file
```

## Covered Scenarios

The test suite includes the following scenarios:

**Positive:**
- Successful user login.
- Adding a single item to the shopping cart.
- Adding multiple items to the shopping cart.
- Removing an item from the shopping cart.
- Successful end-to-end checkout process.

**Negative:**
- Attempting to log in with an invalid password.

**Validation:**
- Attempting to checkout without filling in required personal information.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Allure Commandline:**
    Follow the instructions for your operating system from the official Allure documentation: [Install Allure](https://allurereport.org/docs/gettingstarted-installation/)

## Running Tests

You can run tests using `pytest`. You can run all tests or target specific markers (`positive`, `negative`, `validation`). It's recommended to clean previous Allure results before each run.

1.  **Clean and run all tests:**
    ```bash
    rm -rf allure-results && pytest --alluredir=allure-results
    ```

2.  **Clean and run only positive tests:**
    ```bash
    rm -rf allure-results && pytest -m positive --alluredir=allure-results
    ```

3.  **Clean and run only negative tests:**
    ```bash
    rm -rf allure-results && pytest -m negative --alluredir=allure-results
    ```

4.  **Clean and run only validation tests:**
    ```bash
    rm -rf allure-results && pytest -m validation --alluredir=allure-results
    ```

## Generating the Allure Report

After running the tests with the `--alluredir` flag, you can generate and view the HTML report.

1.  **Generate the report:**
    ```bash
    allure generate allure-results --clean -o allure-report
    ```

2.  **Serve the report:**
    This command will open the report in your default web browser.
    ```bash
    allure serve allure-results
    ```
