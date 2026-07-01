class HomePageLocators:
    """Locators for the ParaBank home / login page."""
    USERNAME_FIELD   = 'input[name="username"]'
    PASSWORD_FIELD   = 'input[name="password"]'
    LOGIN_BUTTON     = 'input[value="Log In"]'
    REGISTER_LINK    = 'a[href*="register"]'
    LOGIN_ERROR      = '.error'