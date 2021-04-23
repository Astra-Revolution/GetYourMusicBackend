Feature: Confirm a contract proposal
  As a musician
  I want to read and review the contract to know
  what I am going to work on

  Scenario: The received contract is accepted
    Given A musician who receives a contract proposal from an event organizer
    When Press the option "accept contract"
    Then a message is displayed with the question "Are you sure you accept this contract" it is confirmed again
    And the list of accepted contracts is shown to the musician

  Scenario: The received contract is rejected
    Given A musician who receives a contract proposal from an event organizer
    When Press the option "reject contract"
    Then a message is displayed with the question "Are you sure to reject this contract", it is confirmed again
    And the list of rejected contracts is shown to the musician