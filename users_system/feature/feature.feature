Feature: Add an user

As a user
I want to register
So I can access to all that get your music offers to me

  Scenario: Creation of a successful user
  Given I have entered my data to register
  When I press register and set a complete request Body
  Then the result should be HTTP response code 201

  Scenario: Error when creating an user
  Given I have entered my incomplete data to register
  When I press register and set a incomplete request Body
  Then the result should be HTTP response code 400
