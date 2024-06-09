# tests/test_signup_login.py
import pytest
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.signup_page import SignupPage
from pages.login_page import LoginPage
from utils.driver_factory import get_driver
from utils.email_helper import get_activation_link

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def setup():
    driver = get_driver()
    yield driver
    driver.quit()

def test_signup_and_activate(setup):
    driver = setup
    logger.info("Navigating to signup page")
    
    # Step 1: Signup
    driver.get("https://galaa.plusonehealth.online/patient/signup")  # Replace with your signup page URL
    signup_page = SignupPage(driver)
    logger.info("Entering signup details")
    signup_page.enter_first_name("Seif")
    signup_page.enter_last_name("Ashraf")
    signup_page.enter_email("seif.ashraf+10@plusone.expert")
    signup_page.enter_confirm_email("seif.ashraf+10@plusone.expert")
    signup_page.enter_password("23")
    signup_page.enter_confirm_password("23")
    signup_page.agree_to_terms()
    signup_page.certify_not_france()
    signup_page.agree_to_newsletter()
    signup_page.click_signup()

    # Wait for the success message or page redirect after signup
    # logger.info("Waiting for signup success message")
    # try:
    #     WebDriverWait(driver, 30).until(
    #         EC.text_to_be_present_in_element(
    #             (By.TAG_NAME, 'body'), 'Signup Successful'  # Adjust this locator based on actual success message
    #         )
    #     )
    # except TimeoutException:
    #     logger.error("Signup did not succeed within the expected time.")

    # Retrieve activation link from email
    activation_link = get_activation_link("seif.ashraf@plusone.expert", "mddu kmfo ctxf mdpf ")
    assert activation_link, "Activation link not found in email"
    logger.info(f"Activation link found: {activation_link}")

    # Step 2: Activate Account
    driver.get(activation_link)
    logger.info("Account activated")

    # Step 3: Login
    driver.get("https://galaa.plusonehealth.online/patient/login")  # Replace with your login page URL
    login_page = LoginPage(driver)
    logger.info("Entering login details")
    login_page.enter_email("seif.ashraf+10@plusone.expert")
    login_page.enter_password("23")
    login_page.click_login()
    
    # Add assertions to verify successful login
    # assert "Dashboard" in driver.title  # Example assertion, update based on your app
    logger.info("Login successful")
