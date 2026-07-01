import time

import pytest
from pytest_bdd import given, when, then, scenarios, parsers
from playwright.sync_api import Page
from locators.homepage import HomePageLocators
from locators.registrationPage import RegistrationPageLocators
from locators.accountOverviewPage import AccountOverviewLocators
from utils.test_data import get_valid_registration_data, get_duplicate_username_data, get_mismatched_password_data, get_spaces_username_data, get_special_char_registration_data, get_all_special_char_data, get_existing_user_credentials


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

def print_account_balances(page: Page):
    """
    Reads the account balance table from the Account Overview page
    and prints a formatted summary to the console.
    This satisfies the requirement: 'log/print the amount post-login'.
    """
    print("\n")
    print("=" * 55)
    print("   POST-LOGIN ACCOUNT BALANCE SUMMARY")
    print("=" * 55)

    rows = page.locator(AccountOverviewLocators.ACCOUNT_ROWS)
    row_count = rows.count()

    if row_count == 0:
        print("   No account data found in the balance table.")
    else:
        for i in range(row_count):
            row = rows.nth(i)
            cells = row.locator("td")
            if cells.count() >= 2:
                account_id       = cells.nth(0).inner_text().strip()
                balance          = cells.nth(1).inner_text().strip()
                available_balance = cells.nth(2).inner_text().strip() if cells.count() > 2 else balance
                print(f"   Account ID        : {account_id}")
                print(f"   Balance           : {balance}")
                print(f"   Available Balance : {available_balance}")
                print("-" * 55)

    print("=" * 55)
    print("\n")



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
def fill_valid_registration_form(page: Page, ctx: dict):
    """Fill all registration fields with valid data from test_data.py."""
    user_data = get_valid_registration_data()
    ctx["user_data"] = user_data
    fill_registration_form(page, user_data)
    print(f"\n[INFO] Attempting registration with username: {user_data['username']}")

@when("I submit the registration form")
def submit_registration_form(page: Page):
    """Click the Register button to submit the form."""

    # Wait for all fields to populate before submitting
    page.wait_for_timeout(2000)  # 2 seconds
    page.click(RegistrationPageLocators.REGISTER_BUTTON)
    page.wait_for_load_state("domcontentloaded")

@when("I fill the registration form with an already registered username")
def fill_duplicate_username_form(page: Page):
    """Fill the form using a username that is already taken — TC_02."""
    user_data = get_duplicate_username_data()
    fill_registration_form(page, user_data)

@when("I submit the registration form without filling any fields")
def submit_empty_registration_form(page: Page):
    """Submit the form with all fields empty — TC_03."""
    page.click(RegistrationPageLocators.REGISTER_BUTTON)
    page.wait_for_load_state("domcontentloaded")

@when("I fill the registration form with mismatched passwords")
def fill_mismatched_password_form(page: Page):
    """Fill the form with two different passwords — TC_04."""
    user_data = get_mismatched_password_data()
    fill_registration_form(page, user_data)

@when("I fill the registration form with spaces as username")
def fill_spaces_username_form(page: Page):
    """Fill the form where username is only whitespace characters — TC_05."""
    user_data = get_spaces_username_data()
    fill_registration_form(page, user_data)

@when(parsers.parse('I enter username "{username}" and password "{password}"'))
def enter_login_credentials(page: Page, username: str, password: str):
    """Type a specific username and password into the login form."""
    page.fill(HomePageLocators.USERNAME_FIELD, username)
    page.fill(HomePageLocators.PASSWORD_FIELD, password)

@when("I click the Log In button")
def click_login_button(page: Page):
    """Click the Log In button and wait for the page to respond."""
    page.click(HomePageLocators.LOGIN_BUTTON)
    page.wait_for_load_state("domcontentloaded")

@when("I leave the login fields empty")
def leave_login_fields_empty(page: Page):
    """Leave both login fields blank — TC_09."""
    # Fields are already empty on page load; nothing to do here
    pass


@when(parsers.parse('I leave the username empty and enter password "{password}"'))
def leave_username_empty_enter_password(page: Page, password: str):
    """Leave username blank but type a password — TC_11."""
    page.fill(HomePageLocators.PASSWORD_FIELD, password)


@when(parsers.parse('I fill the registration form with special characters "{special_chars}" in the "{field_name}" field'))
def fill_special_chars_in_one_field(page: Page, special_chars: str, field_name: str):
    """
    Fill one specific field with special characters, rest with valid data.
    Used in TC_14 to TC_22 — each scenario targets a different field.
    """
    user_data = get_special_char_registration_data(field_name, special_chars)
    fill_registration_form(page, user_data)
    print(f"\n[INFO] Testing field '{field_name}' with value: {special_chars}")

@when(parsers.parse('I fill all registration fields with special characters "{special_chars}"'))
def fill_all_fields_with_special_chars(page: Page, special_chars: str):
    """Fill every single registration field with special characters — TC_23."""
    user_data = get_all_special_char_data(special_chars)
    fill_registration_form(page, user_data)
    print(f"\n[INFO] All fields filled with special characters: {special_chars}")

@when("I click on Account Overview from the Account Service section")
def click_account_overview_link(page: Page):
    """Click Account Overview link in the left Account Service panel."""
    page.click(AccountOverviewLocators.ACCOUNT_OVERVIEW_LINK)
    page.wait_for_load_state("domcontentloaded")

@when("I click the Log Out link")
def click_logout_link(page: Page):
    """Click Log Out to end the current session — TC_13."""
    page.click(AccountOverviewLocators.LOGOUT_LINK)
    page.wait_for_load_state("domcontentloaded")

@when("I enter the registered username and password")
def enter_registered_credentials(page: Page, ctx: dict):
    """
    Re-enter the credentials used during registration.
    Pulls the username from context saved during the registration step.
    """
    user_data = ctx.get("user_data") or get_existing_user_credentials()
    page.fill(HomePageLocators.USERNAME_FIELD, user_data["username"])
    page.fill(HomePageLocators.PASSWORD_FIELD, user_data.get("password", user_data.get("confirm_password", "")))


# ==============================================================
# THEN STEPS — Verifying outcomes / assertions
# ==============================================================

@then("I should see the welcome message with username")
def verify_welcome_message(page: Page):
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
def verify_all_field_errors(page: Page):
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
    """
    TC_05 - Verify an error is shown for spaces-only username.
    The error should be about invalid/blank username.
    It should NOT be 'username already exists' — that would mean
    the server accepted the spaces and tried to register, which is itself a bug.
    """
    error_locator = page.locator(RegistrationPageLocators.USERNAME_ERROR)
    all_errors    = page.locator(RegistrationPageLocators.ALL_ERRORS)

    error_text = ""
    if error_locator.count() > 0:
        error_text = error_locator.inner_text().strip()
    elif all_errors.count() > 0:
        error_text = all_errors.first.inner_text().strip()

    # Fail if no error at all
    assert error_text != "", \
        "Expected a username validation error for spaces-only input but got none."

    # Fail if the wrong error is shown — spaces should not reach the duplicate check
    assert "already" not in error_text.lower(), \
        f"[BUG] Server accepted spaces as a username and hit duplicate check. " \
        f"Expected a blank/invalid username error. Got: '{error_text}'"

    print(f"\n[PASS] Correct username validation error shown: '{error_text}'")


@then("I should be redirected to the Account Overview page")
def verify_account_overview_page(page: Page):
    """Verify successful login redirects to the Account Overview page."""
    assert page.locator(AccountOverviewLocators.LOGOUT_LINK).is_visible() or \
           page.locator(AccountOverviewLocators.ACCOUNT_SERVICE_SECTION).is_visible(), \
        "Expected Account Overview page after login but it was not found."

@then("the Account Service section should be visible")
def verify_account_service_section(page: Page):
    """Confirm the left-panel Account Service section is visible post-login."""
    assert page.locator(AccountOverviewLocators.ACCOUNT_SERVICE_SECTION).is_visible(), \
        "Account Service section is not visible on the page."

@then("I should see the account balance table with Account ID and Balance")
def verify_balance_table_visible(page: Page):
    """Verify the account balance table exists and has at least one row."""
    # Wait until the table appears on the page (max 10 seconds)

    table = page.locator(AccountOverviewLocators.ACCOUNT_TABLE)

    assert table.is_visible(), \
        "Account balance table is not visible on the Account Overview page."

    # Wait until at least one row appears inside the table
    page.wait_for_selector(
        AccountOverviewLocators.ACCOUNT_ROWS,
        timeout=10000
    )

    row_count = page.locator(AccountOverviewLocators.ACCOUNT_ROWS).count()
    assert row_count > 0, \
        "Account balance table is visible but has no rows."

    print(f"\n[PASS] Account balance table visible with {row_count} account(s).")



@then("I should print the account balance details to console")
def print_balance_to_console(page: Page):
    """
    Read and print all account balances from the overview table.
    This directly satisfies the assignment requirement:
    'log/print the amount displayed on the page post-login'.
    """
    print_account_balances(page)

@then(parsers.parse('the system should reject the input and show a validation error for "{field_name}"'))
def verify_special_char_rejected_for_field(page: Page, field_name: str):
    """
    TC_14 to TC_22 - Verify that special character input in a specific field
    is rejected with a validation error.

    BUG NOTE: ParaBank currently DOES NOT reject special characters.
    It accepts them and creates the account. These tests are expected to FAIL,
    which highlights the validation defect in the application.
    """
    # Check if we were redirected to a success page (bug - should NOT happen)
    heading = page.locator(RegistrationPageLocators.SUCCESS_HEADING)
    heading_text = heading.inner_text().strip() if heading.count() > 0 else ""

    if "Welcome" in heading_text:
        # Application accepted special chars — this is the BUG we are reporting
        pytest.fail(
            f"[BUG FOUND] Field '{field_name}' accepted special character input. "
            f"Account was created successfully instead of showing a validation error. "
            f"ParaBank should reject special-character-only values in '{field_name}'."
        )

    # If not redirected to success, check for a validation error message
    error_selector = RegistrationPageLocators.FIELD_ERROR_MAP.get(field_name,
                     RegistrationPageLocators.ALL_ERRORS)
    error_locator  = page.locator(error_selector)
    error_text     = error_locator.inner_text().strip() if error_locator.count() > 0 else ""

    assert error_text != "", \
        f"Expected a validation error for field '{field_name}' with special char input. " \
        f"Neither an error nor a redirect occurred."

    print(f"\n[PASS] Field '{field_name}' correctly rejected special chars. Error: '{error_text}'")



@then("the system should reject the entire form with validation errors for all fields")
def verify_all_special_char_form_rejected(page: Page):
    """
    TC_23 - Verify that submitting all fields with special characters is rejected.

    BUG NOTE: Same as above — ParaBank currently accepts this. Test will FAIL
    to document the defect.
    """
    heading = page.locator(RegistrationPageLocators.SUCCESS_HEADING)
    heading_text = heading.inner_text().strip() if heading.count() > 0 else ""
    if "Welcome" in heading_text:
        pytest.fail(
            "[BUG FOUND] All fields filled with special characters were accepted. "
            "Account was created successfully. "
            "The system should reject a form where every field contains only special characters."
        )

    # If correctly rejected, count how many errors appear
    all_errors = page.locator(RegistrationPageLocators.ALL_ERRORS)
    error_count = all_errors.count()

    assert error_count > 0, \
        "Form was not submitted but no validation errors were shown either."

    print(f"\n[PASS] Entire form with special chars rejected. {error_count} error(s) displayed.")