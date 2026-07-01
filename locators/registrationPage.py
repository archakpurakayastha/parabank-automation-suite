class RegistrationPageLocators:
    """Locators for the ParaBank registration / sign-up form."""

    FIRST_NAME       = 'input[id="customer.firstName"]'
    LAST_NAME        = 'input[id="customer.lastName"]'
    ADDRESS          = 'input[id="customer.address.street"]'
    CITY             = 'input[id="customer.address.city"]'
    STATE            = 'input[id="customer.address.state"]'
    ZIP_CODE         = 'input[id="customer.address.zipCode"]'
    PHONE            = 'input[id="customer.phoneNumber"]'
    SSN              = 'input[id="customer.ssn"]'
    USERNAME         = 'input[id="customer.username"]'
    PASSWORD         = 'input[id="customer.password"]'
    CONFIRM_PASSWORD = 'input[id="repeatedPassword"]'
    REGISTER_BUTTON  = 'input[value="Register"]'

    # Success and error elements
    SUCCESS_HEADING  = '#rightPanel h1'
    SUCCESS_MESSAGE  = '#rightPanel p'
    ALL_ERRORS       = '.error'
    USERNAME_ERROR   = 'span[id="customer.username.errors"]'
    PASSWORD_ERROR   = 'span[id="repeatedPassword.errors"]'

    # Field-specific error span IDs (used for special char validation)
    FIELD_ERROR_MAP = {
        "firstName": 'span[id="customer.firstName.errors"]',
        "lastName": 'span[id="customer.lastName.errors"]',
        "address": 'span[id="customer.address.street.errors"]',
        "city": 'span[id="customer.address.city.errors"]',
        "state": 'span[id="customer.address.state.errors"]',
        "zipCode": 'span[id="customer.address.zipCode.errors"]',
        "phone": 'span[id="customer.phoneNumber.errors"]',
        "ssn": 'span[id="customer.ssn.errors"]',
        "username": 'span[id="customer.username.errors"]',
        "password": 'span[id="customer.password.errors"]',
        "repeatpassword": 'span[id="repeatedPassword.errors"]',
    }
