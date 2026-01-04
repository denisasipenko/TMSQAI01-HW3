from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils.logger import get_logger

# Get logger for the base_page module
logger = get_logger(__name__)


class BasePage:
    """
    The base class for all Page Objects.
    """

    def __init__(self, driver: WebDriver):
        """
        Initializes the BasePage with a WebDriver instance.
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def find_element(self, by, value) -> WebElement:
        """
        Finds a web element with explicit wait.
        """
        logger.info(f"Finding element with locator: {by}='{value}'")
        try:
            element = self.wait.until(EC.presence_of_element_located((by, value)))
            logger.info(f"Element found: {by}='{value}'")
            return element
        except TimeoutException:
            logger.error(f"Element not found within timeout: {by}='{value}'")
            raise

    def find_elements(self, by, value) -> list[WebElement]:
        """
        Finds multiple web elements with explicit wait.
        """
        logger.info(f"Finding elements with locator: {by}='{value}'")
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located((by, value)))
            logger.info(f"Found {len(elements)} elements: {by}='{value}'")
            return elements
        except TimeoutException:
            logger.error(f"Elements not found within timeout: {by}='{value}'")
            raise

    def click(self, by, value):
        """
        Clicks a web element after ensuring it's clickable.
        """
        logger.info(f"Clicking element with locator: {by}='{value}'")
        try:
            element = self.wait.until(EC.element_to_be_clickable((by, value)))
            element.click()
            logger.info(f"Clicked element: {by}='{value}'")
        except TimeoutException:
            logger.error(f"Element not clickable within timeout: {by}='{value}'")
            raise

    def send_keys(self, by, value, text: str):
        """
        Sends text to a web element.
        """
        logger.info(f"Sending keys '{text}' to element: {by}='{value}'")
        try:
            element = self.find_element(by, value)
            element.clear()
            element.send_keys(text)
            logger.info(f"Keys sent successfully to: {by}='{value}'")
        except Exception as e:
            logger.error(f"Error sending keys to {by}='{value}': {e}")
            raise

    def get_text(self, by, value) -> str:
        """
        Gets the text of a web element.
        """
        logger.info(f"Getting text from element: {by}='{value}'")
        try:
            element = self.find_element(by, value)
            text = element.text
            logger.info(f"Got text '{text}' from: {by}='{value}'")
            return text
        except Exception as e:
            logger.error(f"Error getting text from {by}='{value}': {e}")
            raise

    def get_current_url(self) -> str:
        """
        Gets the current URL of the web page.
        """
        logger.info("Getting current URL")
        url = self.driver.current_url
        logger.info(f"Current URL is: {url}")
        return url

    def js_click(self, by, value):
        """
        Clicks a web element using JavaScript.
        """
        logger.info(f"Clicking element with JavaScript: {by}='{value}'")
        try:
            element = self.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", element)
            logger.info(f"Clicked element with JavaScript: {by}='{value}'")
        except Exception as e:
            logger.error(f"Error clicking element with JavaScript {by}='{value}': {e}")
            raise
