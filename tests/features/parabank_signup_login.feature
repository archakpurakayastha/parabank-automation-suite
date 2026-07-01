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