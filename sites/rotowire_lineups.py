from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def open_rotowire_lineups(driver):
    """
    Open the RotoWire Lineups page

    :param driver: Selenium WebDriver object
    """
    driver.get('https://www.rotowire.com/basketball/nba-lineups.php')

def open_rotowire_lineups_in_new_tab(driver):
    """
    Open the RotoWire Lineups page in a new tab

    :param driver: Selenium WebDriver object
    """
    driver.execute_script("window.open('https://www.rotowire.com/basketball/nba-lineups.php', target='_blank')")
    driver.switch_to.window(driver.window_handles[-1])

# Need to check for only games that occur after a specific time
def get_visiting_players(driver):
    """
    Get the names of all players on visiting teams
    
    :param driver: Selenium WebDriver object
    :returns: List containing the names of all players on visiting teams
    """
    current_url = driver.current_url

    if current_url == 'https://www.rotowire.com/basketball/nba-lineups.php':
        visiting_players = driver.find_elements_by_xpath("//ul[contains(@class, 'is-visit')]/li[contains(@class, 'lineup__player')][position()<6]/a")
        for i in range(0, len(visiting_players)):
            visiting_players[i] = visiting_players[i].get_attribute('title')
        print(visiting_players)
        return visiting_players
    else:
        print("Wrong webpage in use. Unable to get players on visiting teams.")

# Need to check for only games that occur after a specific time
def get_home_players(driver):
    """
    Get the names of all players on home teams

    :param driver: Selenium WebDriver object
    :returns: List containing the names of all players on home teams
    """
    current_url = driver.current_url

    if current_url == 'https://www.rotowire.com/basketball/nba-lineups.php':
        home_players = driver.find_elements_by_xpath("//ul[contains(@class, 'is-home')]/li[contains(@class, 'lineup__player')][position()<6]/a")
        for i in range(0, len(home_players)):
            home_players[i] = home_players[i].get_attribute('title')
        print(home_players)
        return home_players
    else:
        print("Wrong webpage in use. Unable to get players on home teams.")

def get_player_links(driver):
    """
    Get the RotoWire hyperlinks of all players currently projected to be in starting lineups

    :param driver: Selenium WebDriver object
    :returns: Dictionary where the names of starting players are mapped to their respective Rotowire hyperlinks
    """
    visiting_player_elements = driver.find_elements_by_xpath("//ul[contains(@class, 'is-visit')]/li[contains(@class, 'lineup__player')][position()<6]/a")
    home_player_elements = driver.find_elements_by_xpath("//ul[contains(@class, 'is-home')]/li[contains(@class, 'lineup__player')][position()<6]/a")
    
    # Store visiting player links first
    player_links = {element.get_attribute('title'): element.get_attribute('href') for element in visiting_player_elements}
    home_player_links = {element.get_attribute('title'): element.get_attribute('href') for element in home_player_elements}
    
    player_links.update(home_player_links)
    return player_links

def get_injured_visiting_players(driver):
    """
    Get the names of all injured players on visiting teams

    :param driver: Selenium WebDriver object
    :returns: List containing the names of all injured players on visiting teams
    """
    current_url = driver.current_url

    if current_url == 'https://www.rotowire.com/basketball/nba-lineups.php':
        visiting_players = driver.find_elements_by_xpath("//ul[contains(@class, 'is-visit')]/li[contains(@class, 'lineup__player')][position()>5]/a")
        for i in range(0, len(visiting_players)):
            visiting_players[i] = visiting_players[i].get_attribute('title')
        print(visiting_players)
        return visiting_players
    else:
        print("Wrong webpage in use. Unable to get injured players of visiting teams.")

def get_injured_home_players(driver):
    """
    Get the names of all injured players on home teams

    :param driver: Selenium WebDriver object
    :returns: List containing the names of all injured players on home teams
    """
    current_url = driver.current_url

    if current_url == 'https://www.rotowire.com/basketball/nba-lineups.php':
        home_players = driver.find_elements_by_xpath("//ul[contains(@class, 'is-home')]/li[contains(@class, 'lineup__player')][position()>5]/a")
        for i in range(0, len(home_players)):
            home_players[i] = home_players[i].get_attribute('title')
        print(home_players)
        return home_players
    else:
        print("Wrong webpage in use. Unable to get injured players of home teams.")

def get_injured_player_links(driver):
    """
    Get the hyperlinks of all players with an injury designation

    :param driver: Selenium WebDriver object
    :returns: Dictionary where the names of injured players are mapped to their respective Rotowire hyperlinks
    """
    out_injured_visiting_player_elements = driver.find_elements_by_xpath("//ul[contains(@class, 'is-visit')]/li[contains(@class, 'lineup__title')]/following-sibling::li[contains(@class, 'is-pct-play-0')]/a")
    out_injured_home_player_elements = driver.find_elements_by_xpath("//ul[contains(@class, 'is-home')]/li[contains(@class, 'lineup__title')]/following-sibling::li[contains(@class, 'is-pct-play-0')]/a")

    doubtful_injured_visiting_player_elements = driver.find_elements_by_xpath("//ul[contains(@class, 'is-visit')]/li[contains(@class, 'lineup__title')]/following-sibling::li[contains(@class, 'is-pct-play-25')]/a")
    doubtful_injured_home_player_elements = driver.find_elements_by_xpath("//ul[contains(@class, 'is-home')]/li[contains(@class, 'lineup__title')]/following-sibling::li[contains(@class, 'is-pct-play-25')]/a")

    questionable_injured_visiting_player_elements = driver.find_elements_by_xpath("//ul[contains(@class, 'is-visit')]/li[contains(@class, 'lineup__title')]/following-sibling::li[contains(@class, 'is-pct-play-50')]/a")
    questionable_injured_home_player_elements = driver.find_elements_by_xpath("//ul[contains(@class, 'is-home')]/li[contains(@class, 'lineup__title')]/following-sibling::li[contains(@class, 'is-pct-play-50')]/a")
    
    probable_injured_visiting_player_elements = driver.find_elements_by_xpath("//ul[contains(@class, 'is-visit')]/li[contains(@class, 'lineup__title')]/following-sibling::li[contains(@class, 'is-pct-play-75')]/a")
    probable_injured_home_player_elements = driver.find_elements_by_xpath("//ul[contains(@class, 'is-home')]/li[contains(@class, 'lineup__title')]/following-sibling::li[contains(@class, 'is-pct-play-75')]/a")

    # Store visiting player links first
    out_injured_player_links = {element.get_attribute('title'): element.get_attribute('href') for element in out_injured_visiting_player_elements}
    out_home_player_links = {element.get_attribute('title'): element.get_attribute('href') for element in out_injured_home_player_elements}
    out_injured_player_links.update(out_home_player_links)

    doubtful_injured_player_links = {element.get_attribute('title'): element.get_attribute('href') for element in doubtful_injured_visiting_player_elements}
    doubtful_home_player_links = {element.get_attribute('title'): element.get_attribute('href') for element in doubtful_injured_home_player_elements}
    doubtful_injured_player_links.update(doubtful_home_player_links)

    questionable_injured_player_links = {element.get_attribute('title'): element.get_attribute('href') for element in questionable_injured_visiting_player_elements}
    questionable_home_player_links = {element.get_attribute('title'): element.get_attribute('href') for element in questionable_injured_home_player_elements}
    questionable_injured_player_links.update(questionable_home_player_links)

    probable_injured_player_links = {element.get_attribute('title'): element.get_attribute('href') for element in probable_injured_visiting_player_elements}
    probable_home_player_links = {element.get_attribute('title'): element.get_attribute('href') for element in probable_injured_home_player_elements}
    probable_injured_player_links.update(probable_home_player_links)

    return out_injured_player_links, doubtful_injured_player_links, questionable_injured_player_links, probable_injured_player_links
