import pytest
from playwright.sync_api import sync_playwright, Browser, Page


# ── Browser Fixture (session-scoped) ──────────────────────────────────────────
# Launched once for the entire test session and shared across all tests.
# This saves time by not reopening a new browser for every scenario.

@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,                              # set False to watch tests run
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        yield browser
        browser.close()


# ── Page Fixture (function-scoped) ────────────────────────────────────────────
# Each test scenario gets its own fresh browser context and page.
# This ensures no cookies, sessions or state leak between tests.

@pytest.fixture(scope="function")
def page(browser_instance: Browser):
    context = browser_instance.new_context()
    page = context.new_page()
    yield page
    # Cleanup after each test
    page.close()
    context.close()


# ── Shared State Fixture ───────────────────────────────────────────────────────
# A simple dictionary passed between step definitions within one scenario.
# Used to carry data like registered username across Given → When → Then steps.

@pytest.fixture
def ctx():
    return {}
