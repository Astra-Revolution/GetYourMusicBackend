Feature: Filters
  As a contractor
  I want to use search filters to get a
  suitable list of musicians

  Scenario: The name of the musician to search exists
    Given An event organizer in the musicians search view
    When Enter in the search bar by name, the name of one or many existing musicians
    Then a list of musicians profiles that match the name entered is displayed

  Scenario: The name of the musician to search for does not exist
    Given An event organizer in the musicians search view
    When Enter in the search bar by name, the name of a musician that does not exist
    Then a list of suggested musicians' profiles according to the organizer's previous hires is displayed

  Scenario: There are musicians that match the selected filters
    Given An event organizer in the musicians search view
    When Select the search filters you want and there are musicians that match the filters
    Then a list of profiles of musicians with characteristics that match the selected filters is displayed

  Scenario: There are no musicians that match the selected filters
    Given An event organizer in the musicians search view
    When Select the search filters you want and there are musicians that match the filters
    Then a list of suggested musician profiles is displayed with characteristics that match the selected filters