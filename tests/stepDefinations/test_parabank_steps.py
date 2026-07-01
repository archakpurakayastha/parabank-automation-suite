import pytest
from pytest_bdd import given, when, then, scenarios, parsers
from playwright.sync_api import Page
from locators.homepage import HomePageLocators
from locators.registrationPage import RegistrationPageLocators
from locators.accountOverviewPage import AccountOverviewLocators


scenarios("../features/parabank_signup_login.feature")
BASE_URL = "https://parabank.parasoft.com/parabank/index.htm?ConnType=JDBC"

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
    assert page.locator(RegistrationPageLocators.FIRST_NAME).is_visible(), \
        "Registration page did not load after clicking Register."