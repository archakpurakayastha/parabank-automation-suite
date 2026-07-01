
import time

def get_timestamp_suffix() -> str:
    """Returns a short timestamp string to make usernames unique per run."""
    return str(int(time.time()))[-5:]


def get_valid_registration_data() -> dict:
    """
    Returns a complete valid user registration payload.
    Username is dynamically suffixed to avoid duplicate conflicts
    on the shared ParaBank demo environment.
    """
    suffix = get_timestamp_suffix()
    return {
        "first_name"       : "Abyss",
        "last_name"        : "Creed",
        "address"          : "Gandhi Park",
        "city"             : "Kolkata",
        "state"            : "West Bengal",
        "zip_code"         : "700159",
        "phone"            : "9903635870",
        "ssn"              : "123456789",
        "username"         : f"abyss.creed.{suffix}",
        "password"         : "0Abyss1",
        "confirm_password" : "0Abyss1",
    }


def get_existing_user_credentials() -> dict:
    """
    Returns credentials for an already registered user.
    Note: This user must exist on the server before running login tests.
    """
    return {
        "username" : "abyss.creed",
        "password" : "0Abyss1",
    }


def get_duplicate_username_data() -> dict:
    """
    Returns registration data using an already registered username.
    """
    return {
        "first_name"       : "Abyss",
        "last_name"        : "Creed",
        "address"          : "Gandhi Park",
        "city"             : "Kolkata",
        "state"            : "West Bengal",
        "zip_code"         : "700159",
        "phone"            : "9903635870",
        "ssn"              : "123456789",
        "username"         : "abyss.creed",   # already exists
        "password"         : "0Abyss1",
        "confirm_password" : "0Abyss1",
    }


def get_mismatched_password_data() -> dict:
    """
    Returns registration data with non-matching passwords.
    """
    suffix = get_timestamp_suffix()
    return {
        "first_name"       : "Abyss",
        "last_name"        : "Creed",
        "address"          : "Gandhi Park",
        "city"             : "Kolkata",
        "state"            : "West Bengal",
        "zip_code"         : "700159",
        "phone"            : "9903635870",
        "ssn"              : "123456789",
        "username"         : f"abyss.mismatch.{suffix}",
        "password"         : "SecurePass@123",
        "confirm_password" : "DifferentPass@456",
    }


def get_spaces_username_data() -> dict:
    """
    Returns registration data where username is only spaces.
    """
    return {
        "first_name"       : "Abyss",
        "last_name"        : "Creed",
        "address"          : "Gandhi Park",
        "city"             : "Kolkata",
        "state"            : "West Bengal",
        "zip_code"         : "700159",
        "phone"            : "9903635870",
        "ssn"              : "123456789",
        "username"         : "   ",           # spaces only
        "password"         : "0Abyss1",
        "confirm_password" : "0Abyss1",
    }


def get_invalid_login_credentials() -> dict:
    """
    Returns credentials that do not exist on the system.
    """
    return {
        "username" : "nonexistent_user_xyz",
        "password" : "WrongPassword999",
    }


def get_wrong_password_data() -> dict:
    """
    Returns a valid username with an incorrect password.
    """
    return {
        "username" : "abyss.creed",
        "password" : "0891",               # wrong password
    }


def get_special_char_registration_data(field: str, special_chars: str) -> dict:
    """
    Returns a registration payload where one specific field
    is filled with special characters, everything else is valid.


    Args:
        field        : The field name to inject special chars into
                       (e.g. 'firstName', 'zipCode')
        special_chars: The special character string to inject
    """
    suffix = get_timestamp_suffix()
    base_data = {
        "first_name"       : "Abyss",
        "last_name"        : "Creed",
        "address"          : "Gandhi Park",
        "city"             : "Kolkata",
        "state"            : "West Bengal",
        "zip_code"         : "700159",
        "phone"            : "9903635870",
        "ssn"              : "123456789",
        "username"         : f"abyss.special.{suffix}",
        "password"         : "0Abyss1",
        "confirm_password" : "0Abyss1",
    }

    # Map feature-file field names to data dict keys
    field_key_map = {
        "firstName" : "first_name",
        "lastName"  : "last_name",
        "address"   : "address",
        "city"      : "city",
        "state"     : "state",
        "zipCode"   : "zip_code",
        "phone"     : "phone",
        "ssn"       : "ssn",
        "username"  : "username",
        "password"  : "password",
    }

    key = field_key_map.get(field)
    if key:
        base_data[key] = special_chars

    return base_data


def get_all_special_char_data(special_chars: str = "@#$") -> dict:
    """
    Returns a registration payload where every single field
    contains only special characters.
    """
    return {
        "first_name"       : special_chars,
        "last_name"        : special_chars,
        "address"          : special_chars,
        "city"             : special_chars,
        "state"            : special_chars,
        "zip_code"         : special_chars,
        "phone"            : special_chars,
        "ssn"              : special_chars,
        "username"         : special_chars,
        "password"         : special_chars,
        "confirm_password" : special_chars,
    }
