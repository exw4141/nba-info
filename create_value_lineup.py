from selenium import webdriver
from selenium.common.exceptions import TimeoutException

import sites.rotowire_lineup_optimizer as lineup_optimizer

import re

import time

class Player:

    def __init__(self, name, positions, salary):
        self._name = name
        self._positions = positions
        self._salary = int(salary[1:])
        self._projected_points = self._salary / 1000 * 5

    def __str__(self):
        return "{}, {}, ${}, {}".format(self._name, self._positions, self._salary, self._projected_points)

    def __repr__(self):
        return "{}, {}, ${}, {}".format(self._name, self._positions, self._salary, self._projected_points)

    @property
    def name(self):
        return self._name

    @property
    def positions(self):
        return self._positions

    @property
    def salary(self):
        return self._salary

    @property
    def projected_points(self):
        return self._projected_points

def create_value_lineup(driver):
    """
    Creates a base lineup of value picks from the highest projected value players on Rotowire's NBA Lineup Optimizer
    :param driver: Selenium WebDriver object
    :returns: A dictionary representing a roster of players projected to be strong value plays for today's classic DFS basketball slate
    """
    roster = {
        'PG': None,
        'SG': None,
        'SF': None,
        'PF': None,
        'C': None,
        'G': None,
        'F': None,
        'UTIL': None
    }
    
    try:
        player_names = lineup_optimizer.get_player_names(driver)
        player_positions = lineup_optimizer.get_player_positions(driver)
        player_salaries = lineup_optimizer.get_player_salaries(driver)
    except TimeoutException:
        print('Unable to get player info. Quitting program.')
        quit()

    num_players = len(player_names)
    for i in range(0, num_players):
        name = player_names[i]
        position = player_positions[i]
        salary = player_salaries[i]
        
        if '/' in position:
            possible_positions = re.findall('[PGSFC]{1,2}', position)[1:]
        else:
            possible_positions = [position]

        player = Player(name, possible_positions, salary)

        roster = process_player_position(roster, player)

        if None not in roster.values():
            break
    return roster

def process_player_position(roster, player):
    """
    Adds a player to the given roster
    :param roster: Dictionary of players who are considered to be strong value plays
    :param player: Player object to be added to the given roster
    :returns: The given roster with the given player added to it. If the player can't be added to the roster, the roster will be returned as it was inputted.
    """
    positions = player.positions

    # Iterate through all possible positions first between checking if flexible positions (G, F, UTIL) are open
    for position in positions:
        if roster[position] is None:
            roster[position] = player
            return roster

    for position in positions:
        if position == 'PG' or position == 'SG':
            if roster['G'] is None:
                roster['G'] = player
                return roster
            elif roster['UTIL'] is None:
                roster['UTIL'] = player
                return roster
        elif position == 'SF' or position == 'PF':
            if roster['F'] is None:
                roster['F'] = player
                return roster
            elif roster['UTIL'] is None:
                roster['UTIL'] = player
                return roster
        elif roster['UTIL'] is None:
            roster['UTIL'] = player
            return roster
    return roster

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()

    lineup_optimizer.open_rotowire_lineup_optimizer(driver)
    lineup_optimizer.sort_players_by_value(driver)

    roster = create_value_lineup(driver)
    print(roster)

    time.sleep(5)
    driver.quit()
