# tests/test_signup_login.py
import pytest
import logging
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.signup_page import SignupPage
from pages.login_page import LoginPage
from pages.demographics_page import DemographicsPage
from utils.driver_factory import get_driver
from utils.email_helper import get_activation_link

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SIGNUP_URL = "https://galaa.plusonehealth.online/patient/signup"
LOGIN_URL = "https://galaa.plusonehealth.online/patient/login"
NEWCASE_URL = "https://galaa.plusonehealth.online/patient/newcase"
EMAIL = "seif.ashraf+54@plusone.expert"
PASSWORD = "Password@123"

@pytest.fixture(scope="module")
def setup():
    driver = get_driver()
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def gmail_password():
    return os.getenv('GMAIL_PASSWORD')

@pytest.mark.run(order=1)
def test_signup_login_and_activate(setup, gmail_password):
    driver = setup
    logger.info("Navigating to signup page")
    
    # Step 1: Signup
    driver.get(SIGNUP_URL)
    signup_page = SignupPage(driver)
    logger.info("Entering signup details")
    signup_page.enter_first_name("Seif")
    signup_page.enter_last_name("Ashraf")
    signup_page.enter_email(EMAIL)
    signup_page.enter_confirm_email(EMAIL)
    signup_page.enter_password(PASSWORD)
    signup_page.enter_confirm_password(PASSWORD)
    signup_page.agree_to_terms()
    signup_page.certify_not_france()
    signup_page.agree_to_newsletter()
    signup_page.click_signup()

    # Retrieve activation link from email
    logger.info("Retrieving activation link from email")
    activation_link = get_activation_link(EMAIL, gmail_password)
    assert activation_link, "Activation link not found in email"
    logger.info(f"Activation link found: {activation_link}")

    # Step 2: Activate Account
    logger.info("Activating account")
    driver.get(activation_link)
    
    logger.info("Account activated")

    # Step 3: Login
    logger.info("Navigating to login page")
    driver.get(LOGIN_URL)
    login_page = LoginPage(driver)
    logger.info("Entering login details")
    login_page.enter_email(EMAIL)
    login_page.enter_password(PASSWORD)
    login_page.click_login()

    logger.info("Waiting for page redirect after login")
    try:
        WebDriverWait(driver, 60).until(EC.url_to_be(NEWCASE_URL))
    except TimeoutException:
        logger.error("Login did not succeed within the expected time.")
        pytest.fail("Login did not succeed within the expected time.")
    
    logger.info("Login successful")

@pytest.mark.run(order=2)
def test_fill_demographics(setup):
    driver = setup

    logger.info("Navigating to demographics form")
    driver.get(NEWCASE_URL)
    demographics_page = DemographicsPage(driver)
    logger.info("Entering demographics details")

    logger.info("Selecting the phone country code")
    demographics_page.select_phone_country_code("Aland")  # Replace with the desired country code
    demographics_page.enter_phone("1234567890")

    demographics_page.enter_dob("1990-01-01")
    demographics_page.enter_weight("70")
    demographics_page.enter_height("180")
    demographics_page.enter_city("Test City")
    demographics_page.enter_zip("12345")
    demographics_page.enter_address("123 Test Street")
    
    logger.info("Selecting the country")
    demographics_page.select_country("United States")  # Replace with the desired country

    logger.info("Selecting the gender")
    demographics_page.select_gender("Male")  # Replace with the desired gender

    logger.info("Selecting the blood type")
    demographics_page.select_blood_type("O+")  # Replace with the desired blood type

    logger.info("Submitting the form")
    demographics_page.submit_form()
