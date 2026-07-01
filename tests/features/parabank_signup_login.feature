Feature: ParaBank Sign Up and Login Flow

  # ----------------------------------------------------------
  # REGISTRATION SCENARIOS
  # ----------------------------------------------------------

  Background:
    Given I am on the ParaBank home page


  @registration @happy_path @TC_01
  Scenario: TC_01 - Successful registration with valid details
    When I click on the Register link

