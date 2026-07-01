import pytest
import os
import allure
from datetime import datetime
from playwright.sync_api import sync_playwright, Browser, Page


# Screenshots folder — created automatically if it doesn't exist
SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


# ── Browser Fixture (session-scoped) ──────────────────────────────────────────
# Launched once for the entire test session and shared across all tests.
# This saves time by not reopening a new browser for every scenario.

@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,                          # set False to watch tests run
            slow_mo=200, # ← adds 200ms delay between every action
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        yield browser
        browser.close()


# ── Page Fixture (function-scoped) ────────────────────────────────────────────
# Each test scenario gets its own fresh browser context and page.
# This ensures no cookies, sessions or state leak between tests.
# On failure — screenshot is saved to /Screenshots and attached to Allure.

@pytest.fixture(scope="function")
def page(browser_instance: Browser, request):
    context = browser_instance.new_context(
        viewport={"width": 1280, "height": 800}
    )
    page = context.new_page()

    yield page

    # ── After each test: check if it failed ───────────────────────────────────
    # request.node.rep_call is set by the pytest_runtest_makereport hook below.
    # If the test failed, capture a screenshot.

    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed

    if failed:
        # Build a clean filename using test name + timestamp
        test_name  = request.node.name.replace(" ", "_").replace("/", "_")
        timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename   = f"FAILED_{test_name}_{timestamp}.png"
        filepath   = os.path.join(SCREENSHOTS_DIR, filename)

        # Save screenshot to /Screenshots folder
        page.screenshot(path=filepath, full_page=True)
        print(f"\n[SCREENSHOT] Saved to: Screenshots/{filename}")

        # Attach the same screenshot to the Allure report
        with open(filepath, "rb") as f:
            allure.attach(
                f.read(),
                name=f"Failure Screenshot - {test_name}",
                attachment_type=allure.attachment_type.PNG
            )

    # Cleanup
    page.close()
    context.close()


# ── Hook to track pass/fail status per test ───────────────────────────────────
# pytest does not expose pass/fail inside fixtures by default.
# This hook stores the result on the test node so the page fixture can read it.

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Store the result of the actual test call (not setup or teardown)
    if rep.when == "call":
        item.rep_call = rep


# ── Shared State Fixture ───────────────────────────────────────────────────────
# A simple dictionary passed between step definitions within one scenario.
# Used to carry data like registered username across Given → When → Then steps.

@pytest.fixture
def ctx():
    return {}