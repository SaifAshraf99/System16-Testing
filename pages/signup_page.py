from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class SignupPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.first_name_input = (By.CSS_SELECTOR, '[test-id="input-first_name"]')
        self.last_name_input = (By.CSS_SELECTOR, '[test-id="input-last_name"]')
        self.email_input = (By.CSS_SELECTOR, '[test-id="input-email"]')
        self.confirm_email_input = (By.CSS_SELECTOR, '[test-id="input-confirm email"]')
        self.password_input = (By.CSS_SELECTOR, '[test-id="input-password"]')
        self.confirm_password_input = (By.CSS_SELECTOR, '[test-id="input-confirm password"]')
        self.terms_checkbox = (By.CSS_SELECTOR, '[test-id="checkbox-policyaccept"]')
        self.not_france_checkbox = (By.CSS_SELECTOR, '[test-id="checkbox-residence"]')
        self.newsletter_checkbox = (By.CSS_SELECTOR, '[test-id="checkbox-newsletters_updates"]')
        self.signup_button = (By.CSS_SELECTOR, 'button[type="submit"]')

    def enter_first_name(self, first_name):
        print("Entering first name")
        self.wait.until(EC.presence_of_element_located(self.first_name_input)).send_keys(first_name)

    def enter_last_name(self, last_name):
        print("Entering last name")
        self.wait.until(EC.presence_of_element_located(self.last_name_input)).send_keys(last_name)

    def enter_email(self, email):
        print("Entering email")
        self.wait.until(EC.presence_of_element_located(self.email_input)).send_keys(email)

    def enter_confirm_email(self, confirm_email):
        print("Entering confirm email")
        self.wait.until(EC.presence_of_element_located(self.confirm_email_input)).send_keys(confirm_email)

    def enter_password(self, password):
        print("Entering password")
        self.wait.until(EC.presence_of_element_located(self.password_input)).send_keys(password)

    def enter_confirm_password(self, confirm_password):
        print("Entering confirm password")
        self.wait.until(EC.presence_of_element_located(self.confirm_password_input)).send_keys(confirm_password)

    def agree_to_terms(self):
        print("Agreeing to terms")
        try:
            # Locate the parent div which is actually clickable
            element = self.wait.until(EC.presence_of_element_located(self.terms_checkbox))
            self.driver.execute_script("arguments[0].click();", element)
        except TimeoutException:
            print("TimeoutException: Element for agreeing to terms not found.")
        except NoSuchElementException:
            print("NoSuchElementException: Element for agreeing to terms not found.")

    def certify_not_france(self):
        print("Certifying not in France")
        try:
            element = self.wait.until(EC.presence_of_element_located(self.not_france_checkbox))
            self.driver.execute_script("arguments[0].click();", element)
        except TimeoutException:
            print("TimeoutException: Element for certifying not in France not found.")
        except NoSuchElementException:
            print("NoSuchElementException: Element for certifying not in France not found.")

    def agree_to_newsletter(self):
        print("Agreeing to newsletter")
        try:
            element = self.wait.until(EC.presence_of_element_located(self.newsletter_checkbox))
            self.driver.execute_script("arguments[0].click();", element)
        except TimeoutException:
            print("TimeoutException: Element for agreeing to newsletter not found.")
        except NoSuchElementException:
            print("NoSuchElementException: Element for agreeing to newsletter not found.")

    def click_signup(self):
        print("Clicking signup button")
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.signup_button))
            self.driver.execute_script("arguments[0].click();", element)
        except TimeoutException:
            print("TimeoutException: Signup button not clickable.")
        except NoSuchElementException:
            print("NoSuchElementException: Signup button not found.")
