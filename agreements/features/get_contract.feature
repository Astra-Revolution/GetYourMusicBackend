Feature: Visualize a specific contract
  As a musician
  I want visualize my contracts
  So organize my sketch rule

  Scenario: The musician select a contract from the list and can see its details
    Given an musician watching his list of contracts
    When select a available contract
    Then shows the contract's details

  Scenario: The musician select a contract from the list and can't see its details
    Given an musician watching his list of contracts
    When select a unavailable contract
    Then shows the message "Error 404: Contract not founded"