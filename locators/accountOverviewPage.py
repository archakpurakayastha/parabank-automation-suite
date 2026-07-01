class AccountOverviewLocators:
    """Locators for the post-login Account Overview / dashboard page."""
    ACCOUNT_SERVICE_SECTION = '#leftPanel'
    ACCOUNT_OVERVIEW_LINK   = 'a[href*="overview"]'
    ACCOUNT_TABLE           = '#accountTable'
    ACCOUNT_ROWS            = '#accountTable tbody tr'
    LOGOUT_LINK             = 'a[href*="logout"]'
    WELCOME_MESSAGE         = '#leftPanel p.smallText'
    PAGE_HEADER             = '#rightPanel h1'