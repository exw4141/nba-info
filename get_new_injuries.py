from selenium import webdriver
from sites import rotowire_lineups as lineups
from sites import rotowire_player_page as player_page

import time

def process_injured_player_links(driver, injured_player_links):
    """
    Displays names of players who have just recently received an injury designation

    :param driver: Selenium WebDriver object
    :returns: List of the names of players who have just recently received an injury designation
    """
    recently_injured_players = []
    for player in injured_player_links.keys():
        player_link = injured_player_links[player]
        player_page.open_player_page(driver, player_link)
        player_page.scroll_to_game_log(driver)
        
        recently_injured = player_page.get_recently_injured(driver)
        if recently_injured:
            recently_injured_players.append(player)
    return recently_injured_players

def print_injured_player_names(injured_players):
    """
    Prints list of injured players.
    Prints "None" if given list is empty

    :param injured_players: List of the ames of injured players
    """
    if len(injured_players) == 0:
        print('None')
    else:
        for player_name in injured_players:
            print(player_name)
    print()

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()

    lineups.open_rotowire_lineups(driver)
    out_injured_player_links, doubtful_injured_player_links, questionable_injured_player_links, probable_injured_player_links = lineups.get_injured_player_links(driver)

    injured_players = process_injured_player_links(driver, out_injured_player_links)
    print('Out:')
    print_injured_player_names(injured_players)

    injured_players = process_injured_player_links(driver, doubtful_injured_player_links)
    print('Doubtful:')
    print_injured_player_names(injured_players)

    injured_players = process_injured_player_links(driver, questionable_injured_player_links)
    print('Questionable:')
    print_injured_player_names(injured_players)

    injured_players = process_injured_player_links(driver, probable_injured_player_links)
    print('Probable:')
    print_injured_player_names(injured_players)

    time.sleep(3)
    driver.close()
