from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time

logger = logging.getLogger(__name__)

class DemographicsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.phone_dropdown = (By.ID, 'react-select-2-input')
        self.phone_input = (By.NAME, 'mobile')
        self.dob_input = (By.NAME, 'date_of_birth')
        self.weight_input = (By.NAME, 'weight')
        self.height_input = (By.NAME, 'height')
        self.city_input = (By.NAME, 'city')
        self.zip_input = (By.NAME, 'zip')
        self.address_input = (By.NAME, 'address')
        self.country_dropdown = (By.ID, 'react-select-3-input')
        self.gender_dropdown = (By.ID, 'react-select-4-input')
        self.blood_dropdown = (By.ID, 'react-select-5-input')
        self.submit_button = (By.CSS_SELECTOR, 'button[type="submit"]')

    def enter_phone(self, phone):
        logger.info("Entering phone")
        self.wait.until(EC.presence_of_element_located(self.phone_input)).send_keys(phone)

    def enter_dob(self, dob):
        logger.info("Entering date of birth")
        self.wait.until(EC.presence_of_element_located(self.dob_input)).send_keys(dob)

    def enter_weight(self, weight):
        logger.info("Entering weight")
        self.wait.until(EC.presence_of_element_located(self.weight_input)).send_keys(weight)

    def enter_height(self, height):
        logger.info("Entering height")
        self.wait.until(EC.presence_of_element_located(self.height_input)).send_keys(height)

    def enter_city(self, city):
        logger.info("Entering city")
        self.wait.until(EC.presence_of_element_located(self.city_input)).send_keys(city)

    def enter_zip(self, zip_code):
        logger.info("Entering zip code")
        self.wait.until(EC.presence_of_element_located(self.zip_input)).send_keys(zip_code)

    def enter_address(self, address):
        logger.info("Entering address")
        self.wait.until(EC.presence_of_element_located(self.address_input)).send_keys(address)

    def select_option_from_dropdown(self, dropdown_locator, option_value):
        logger.info(f"Selecting option {option_value} from dropdown")
        dropdown_element = self.wait.until(EC.element_to_be_clickable(dropdown_locator))
        dropdown_element.click()  # Open the dropdown

        logger.info("Dropdown clicked, waiting for options to be visible")
        options_container_locator = (By.CSS_SELECTOR, ".css-26l3qy-menu")  # Adjust if necessary

        try:
            self.wait.until(EC.visibility_of_element_located(options_container_locator))
            logger.info("Options container is visible")
        except TimeoutException:
            logger.error("Options container not visible within the timeout period")
            self.driver.save_screenshot(f"dropdown_error_{time.time()}.png")
            raise

        option_locator = (By.XPATH, f"//div[contains(text(), '{option_value}')]")
        try:
            option_element = self.wait.until(EC.element_to_be_clickable(option_locator))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", option_element)
            self.driver.execute_script("arguments[0].click();", option_element)
            logger.info(f"Option {option_value} selected using JavaScript")
        except TimeoutException:
            logger.error(f"Option {option_value} not clickable within the timeout period")
            self.driver.save_screenshot(f"option_error_{time.time()}.png")
            raise

    def select_phone_country_code(self, country_code):
        self.select_option_from_dropdown(self.phone_dropdown, country_code)

    def select_country(self, country):
        self.select_option_from_dropdown(self.country_dropdown, country)

    def select_gender(self, gender):
        self.select_option_from_dropdown(self.gender_dropdown, gender)

    def select_blood_type(self, blood_type):
        self.select_option_from_dropdown(self.blood_dropdown, blood_type)

    def submit_form(self):
        logger.info("Submitting the form")
        self.wait.until(EC.element_to_be_clickable(self.submit_button)).click()
