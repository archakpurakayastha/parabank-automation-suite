Feature: ParaBank Sign Up and Login Flow

  # ----------------------------------------------------------
  # REGISTRATION SCENARIOS
  # ----------------------------------------------------------

  Background:
    Given I am on the ParaBank home page


  @registration @positive_scenario @TC_01
  Scenario: TC_01 - Successful registration with valid details
    When I click on the Register link
    And I fill the registration form with valid user details
    And I submit the registration form
    Then I should see the welcome message with username
    And I should be logged in with Account Service section visible


  @registration @negative_scenario @TC_02
  Scenario: TC_02 - Registration fails when username already exists
    When I click on the Register link
    And I fill the registration form with an already registered username
    And I submit the registration form
    Then I should see the error "This username already exists."


  @registration @negative_scenario @TC_03
  Scenario: TC_03 - Registration fails when all fields are left empty
    When I click on the Register link
    And I submit the registration form without filling any fields
    Then I should see inline validation errors for all required fields


  @registration @negative_scenario @TC_04
  Scenario: TC_04 - Registration fails when password and confirm password do not match
    When I click on the Register link
    And I fill the registration form with mismatched passwords
    And I submit the registration form
    Then I should see the error "Passwords did not match."

  @registration @negative_scenario @TC_05
  Scenario: TC_05 - Registration with spaces only as username
    When I click on the Register link
    And I fill the registration form with spaces as username
    And I submit the registration form
    Then I should see a username validation error

  # ----------------------------------------------------------
  # LOGIN SCENARIOS
  # ----------------------------------------------------------

  @login @positive_scenario @TC_06
  Scenario: TC_06 - Successful login with valid credentials
    When I enter username "abyss.creed" and password "0Abyss1"
    And I click the Log In button
    Then I should be redirected to the Account Overview page
    And the Account Service section should be visible

  @login @positive_scenario @TC_07
  Scenario: TC_07 - Account balance is displayed and printed after login
    When I enter username "abyss.creed" and password "0Abyss1"
    And I click the Log In button
    Then I should see the account balance table with Account ID and Balance
    And I should print the account balance details to console

  @login @negative_scenario @TC_08
  Scenario: TC_08 - Login fails with invalid username and password
    When I enter username "nonexistent_user_xyz" and password "WrongPassword999"
    And I click the Log In button
    Then I should see the error "The username and password could not be verified."

  @login @negative_scenario @TC_09
  Scenario: TC_09 - Login fails when both fields are empty
    When I leave the login fields empty
    And I click the Log In button
    Then I should see the error "Please enter a username and password."

  @login @negative_scenario @TC_10
  Scenario: TC_10 - Login fails with valid username but wrong password
    When I enter username "abyss.creed" and password "0891"
    And I click the Log In button
    Then I should see the error "The username and password could not be verified."

  @login @negative_scenario @TC_11
  Scenario: TC_11 - Login fails when username is empty but password is entered
    When I leave the username empty and enter password "SecurePass@123"
    And I click the Log In button
    Then I should see the error "Please enter a username and password."
    
    
  # ----------------------------------------------------------
  # END-TO-END SCENARIOS
  # ----------------------------------------------------------

  @end_to_end @TC_12
  Scenario: TC_12 - Complete register then navigate to Account Overview and check balance
    Given I am on the ParaBank home page
    When I click on the Register link
    And I fill the registration form with valid user details
    And I submit the registration form
    Then I should see the welcome message with username
    When I click on Account Overview from the Account Service section
    Then I should see the account balance table with Account ID and Balance
    And I should print the account balance details to console

  @end_to_end @TC_13
  Scenario: TC_13 - Register then logout then login again and verify balance
    Given I am on the ParaBank home page
    When I click on the Register link
    And I fill the registration form with valid user details
    And I submit the registration form
    Then I should see the welcome message with username
    When I click the Log Out link
    And I enter the registered username and password
    And I click the Log In button
    Then I should be redirected to the Account Overview page
    And I should see the account balance table with Account ID and Balance

  # ----------------------------------------------------------
  # SPECIAL CHARACTER VALIDATION – REGISTRATION FORM
  # ----------------------------------------------------------

  @special_char @negative_scenario @TC_14
  Scenario: TC_14 - Registration with special characters in First Name
    When I click on the Register link
    And I fill the registration form with special characters "@#$%^&*()" in the "firstName" field
    And I submit the registration form
    Then the system should reject the input and show a validation error for "firstName"

  @special_char @negative_scenario @TC_15
  Scenario: TC_15 - Registration with special characters in Last Name
    When I click on the Register link
    And I fill the registration form with special characters "!@#$%^&*()" in the "lastName" field
    And I submit the registration form
    Then the system should reject the input and show a validation error for "lastName"

  @special_char @negative_scenario @TC_16
  Scenario: TC_16 - Registration with special characters in Address
    When I click on the Register link
    And I fill the registration form with special characters "@#$!%^&*()" in the "address" field
    And I submit the registration form
    Then the system should reject the input and show a validation error for "address"

  @special_char @negative_scenario @TC_17
  Scenario: TC_17 - Registration with special characters in City
    When I click on the Register link
    And I fill the registration form with special characters "###$$$@@@" in the "city" field
    And I submit the registration form
    Then the system should reject the input and show a validation error for "city"

  @special_char @negative_scenario @TC_18
  Scenario: TC_18 - Registration with special characters in State
    When I click on the Register link
    And I fill the registration form with special characters "@#$" in the "state" field
    And I submit the registration form
    Then the system should reject the input and show a validation error for "state"

  @special_char @negative_scenario @TC_19
  Scenario: TC_19 - Registration with special characters in Zip Code
    When I click on the Register link
    And I fill the registration form with special characters "@#$%^" in the "zipCode" field
    And I submit the registration form
    Then the system should reject the input and show a validation error for "zipCode"

  @special_char @negative_scenario @TC_20
  Scenario: TC_20 - Registration with special characters in Phone Number
    When I click on the Register link
    And I fill the registration form with special characters "@#$%^&*()" in the "phone" field
    And I submit the registration form
    Then the system should reject the input and show a validation error for "phone"

  @special_char @negative_scenario @TC_21
  Scenario: TC_21 - Registration with special characters in SSN
    When I click on the Register link
    And I fill the registration form with special characters "@#$-%%^&" in the "ssn" field
    And I submit the registration form
    Then the system should reject the input and show a validation error for "ssn"

  @special_char @negative_scenario @TC_22
  Scenario: TC_22 - Registration with special characters in Username
    When I click on the Register link
    And I fill the registration form with special characters "@#$%^&*()" in the "username" field
    And I submit the registration form
    Then the system should reject the input and show a validation error for "username"

  @special_char @negative_scenario @TC_23
  Scenario: TC_23 - Registration with special characters in all fields simultaneously
    When I click on the Register link
    And I fill all registration fields with special characters "@#$"
    And I submit the registration form
    Then the system should reject the entire form with validation errors for all fields