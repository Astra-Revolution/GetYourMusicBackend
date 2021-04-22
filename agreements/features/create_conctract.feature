Feature: Create a new contract
  As a organizer
  I want create a new contract
  So the musician to participate in my event

  Scenario: The organizer enter valid data and create a contract
    Given an organizer in the register contract form
    When send the form with valid data pushing the button "Create Contract"
    Then create and show it in the list of contracts

  Scenario: The organizer enter invalid data and the new contract can't be created
    Given an organizer in the register contract form
    When send the form with invalid data pushing the button "Create Contract"
    Then show the same form indicating the wrong fields
    And ask to fix them

