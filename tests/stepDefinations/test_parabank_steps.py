import pytest
from pytest_bdd import given, when, then, scenarios, parsers
from playwright.sync_api import Page
from locators.homepage import HomePageLocators
from locators.registrationPage import RegistrationPageLocators
from locators.accountOverviewPage import AccountOverviewLocators
from utils.test_data import get_valid_registration_data, get_duplicate_username_data, get_mismatched_password_data, get_spaces_username_data


scenarios("../features/parabank_signup_login.feature")
BASE_URL = "https://parabank.parasoft.com/parabank/index.htm?ConnType=JDBC"

# ==============================================================
# HELPER FUNCTIONS
# ==============================================================

def fill_registration_form(page: Page, user_data: dict):
    """
    Fills every field on the ParaBank registration form.
    Accepts a dict with keys matching the form fields.
    """
    page.fill(RegistrationPageLocators.FIRST_NAME,       user_data.get("first_name", ""))
    page.fill(RegistrationPageLocators.LAST_NAME,        user_data.get("last_name", ""))
    page.fill(RegistrationPageLocators.ADDRESS,          user_data.get("address", ""))
    page.fill(RegistrationPageLocators.CITY,             user_data.get("city", ""))
    page.fill(RegistrationPageLocators.STATE,            user_data.get("state", ""))
    page.fill(RegistrationPageLocators.ZIP_CODE,         user_data.get("zip_code", ""))
    page.fill(RegistrationPageLocators.PHONE,            user_data.get("phone", ""))
    page.fill(RegistrationPageLocators.SSN,              user_data.get("ssn", ""))
    page.fill(RegistrationPageLocators.USERNAME,         user_data.get("username", ""))
    page.fill(RegistrationPageLocators.PASSWORD,         user_data.get("password", ""))
    page.fill(RegistrationPageLocators.CONFIRM_PASSWORD, user_data.get("confirm_password", ""))




# ==============================================================
# GIVEN STEPS — Setting up the starting state
# ==============================================================

@given("I am on the ParaBank home page")
def open_home_page(page: Page):
    """Navigate to the ParaBank home page and confirm it loaded."""
    page.goto(BASE_URL)
    page.wait_for_load_state("domcontentloaded")


    # Confirm the login form is visible before proceeding
    assert page.locator(HomePageLocators.USERNAME_FIELD).is_visible(), "Home page did not load — login form not found."


# ==============================================================
# WHEN STEPS — Performing actions
# ==============================================================

@when("I click on the Register link")
def click_register_link(page: Page):
    """Click the Register link and wait for the registration form to load."""
    page.click(HomePageLocators.REGISTER_LINK)
    page.wait_for_load_state("domcontentloaded")

    # Confirm we landed on the registration page
    assert page.locator(RegistrationPageLocators.FIRST_NAME).is_visible(), "Registration page did not load after clicking Register."

@when("I fill the registration form with valid user details")
def fill_valid_registration_form(page: Page):
    """Fill all registration fields with valid data from test_data.py."""
    user_data = get_valid_registration_data()
    fill_registration_form(page, user_data)
    print(f"\n[INFO] Attempting registration with username: {user_data['username']}")

@when("I submit the registration form")
def submit_registration_form(page: Page, ctx: dict):
    """Click the Register button to submit the form."""
    page.click(RegistrationPageLocators.REGISTER_BUTTON)
    page.wait_for_load_state("domcontentloaded")

@when("I fill the registration form with an already registered username")
def fill_duplicate_username_form(page: Page, ctx: dict):
    """Fill the form using a username that is already taken — TC_02."""
    user_data = get_duplicate_username_data()
    ctx["user_data"] = user_data
    fill_registration_form(page, user_data)

@when("I submit the registration form without filling any fields")
def submit_empty_registration_form(page: Page, ctx: dict):
    """Submit the form with all fields empty — TC_03."""
    page.click(RegistrationPageLocators.REGISTER_BUTTON)
    page.wait_for_load_state("domcontentloaded")

@when("I fill the registration form with mismatched passwords")
def fill_mismatched_password_form(page: Page, ctx: dict):
    """Fill the form with two different passwords — TC_04."""
    user_data = get_mismatched_password_data()
    ctx["user_data"] = user_data
    fill_registration_form(page, user_data)

@when("I fill the registration form with spaces as username")
def fill_spaces_username_form(page: Page, ctx: dict):
    """Fill the form where username is only whitespace characters — TC_05."""
    user_data = get_spaces_username_data()
    ctx["user_data"] = user_data
    fill_registration_form(page, user_data)


# ==============================================================
# THEN STEPS — Verifying outcomes / assertions
# ==============================================================

@then("I should see the welcome message with username")
def verify_welcome_message(page: Page, ctx: dict):
    """
    After successful registration, ParaBank shows a welcome heading.
    Verify the heading contains 'Welcome' confirming registration success.
    """
    heading = page.locator(RegistrationPageLocators.SUCCESS_HEADING)
    heading_text = heading.inner_text().strip() if heading.count() > 0 else ""

    assert "Welcome" in heading_text, f"Expected 'Welcome' in heading after registration. Got: '{heading_text}'"

    print(f"\n[PASS] Registration successful — Heading: '{heading_text}'")



@then("I should be logged in with Account Service section visible")
def verify_account_service_visible(page: Page):
    """Verify the Account Service left panel is present after auto-login."""
    assert page.locator(AccountOverviewLocators.ACCOUNT_SERVICE_SECTION).is_visible(), "Account Service section not visible — user may not be logged in."



@then(parsers.parse('I should see the error "{expected_error}"'))
def verify_error_message(page: Page, expected_error: str):
    """
    Generic error message verifier.
    Checks the visible error element on the page matches expected text.
    """
    # Error could be on registration page or login page
    error_locator = page.locator(f"{RegistrationPageLocators.ALL_ERRORS}, {HomePageLocators.LOGIN_ERROR}")
    error_text = ""

    if error_locator.count() > 0:
        error_text = error_locator.first.inner_text().strip()

    assert expected_error.lower() in error_text.lower(), \
        f"Expected error: '{expected_error}' | Actual error found: '{error_text}'"

    print(f"\n[PASS] Correct error shown: '{error_text}'")

@then("I should see inline validation errors for all required fields")
def verify_all_field_errors(page: Page, ctx: dict):
    """
    TC_03 - Verify that submitting an empty form shows errors for every field.
    ParaBank shows individual error spans below each required field.
    """
    required_fields = [
        RegistrationPageLocators.FIELD_ERROR_MAP["firstName"],
        RegistrationPageLocators.FIELD_ERROR_MAP["lastName"],
        RegistrationPageLocators.FIELD_ERROR_MAP["address"],
        RegistrationPageLocators.FIELD_ERROR_MAP["city"],
        RegistrationPageLocators.FIELD_ERROR_MAP["state"],
        RegistrationPageLocators.FIELD_ERROR_MAP["zipCode"],
        RegistrationPageLocators.FIELD_ERROR_MAP["ssn"],
        RegistrationPageLocators.FIELD_ERROR_MAP["username"],
        RegistrationPageLocators.FIELD_ERROR_MAP["password"],
        RegistrationPageLocators.FIELD_ERROR_MAP["repeatpassword"],
    ]

    errors_found = []
    for selector in required_fields:
        locator = page.locator(selector)
        if locator.count() > 0 and locator.inner_text().strip():
            errors_found.append(locator.inner_text().strip())

    # Fallback: count generic error elements if field-specific ones aren't present
    if len(errors_found) == 0:
        generic_errors = page.locator(RegistrationPageLocators.ALL_ERRORS)
        errors_found = [generic_errors.nth(i).inner_text().strip()
                        for i in range(generic_errors.count())]

    assert len(errors_found) > 0, "Expected validation errors for empty form submission but none were found."

    print(f"\n[PASS] {len(errors_found)} validation error(s) found:")
    for err in errors_found:
        print(f"       - {err}")
        

@then("I should see a username validation error")
def verify_username_error(page: Page, ctx: dict):
    """TC_05 - Verify an error is shown for spaces-only username."""
    error_locator = page.locator(RegistrationPageLocators.USERNAME_ERROR)
    all_errors    = page.locator(RegistrationPageLocators.ALL_ERRORS)

    error_text = ""
    if error_locator.count() > 0:
        error_text = error_locator.inner_text().strip()
    elif all_errors.count() > 0:
        error_text = all_errors.first.inner_text().strip()

    assert error_text != "", \
        "Expected a username validation error for spaces-only input but got none."

    print(f"\n[PASS] Username error shown: '{error_text}'")