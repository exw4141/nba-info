from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import time

def open_nba_players_page(driver):
    """
    Open ESPN's NBA player statistics page

    :param driver: Selenium WebDriver object
    """
    driver.get('https://www.espn.com/nba/stats/player/_/table/general/sort/avgMinutes/dir/desc')

def get_player_links(driver):
    """
    Get hyperlinks for all players on the player page

    :param driver: Selenium WebDriver object
    """
    current_url = driver.current_url

    if current_url == 'https://www.espn.com/nba/stats/player/_/table/general/sort/avgMinutes/dir/desc':
        player_links = [link.get_attribute('href') for link in driver.find_elements_by_xpath("//td[@class='Table__TD']//a")]
        return player_links
    else:
        print("Wrong webpage in use. Unable to get links of player pages.")

def process_player_game_log(driver):
    current_url = driver.current_url

    if current_url.startswith('https://www.espn.com/nba/player/_/id/'):
        game_log_tab = driver.find_element_by_link_text('Game Log')
        game_log_tab.click()
    else:
        print("Wrong webpage in use. Unable to extract player's game log")

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.maximize_window()

    open_nba_players_page(driver)
    player_links = get_player_links(driver)
    for link in player_links:
        driver.get(link)

        process_player_game_log(driver)
        open_nba_players_page(driver)
