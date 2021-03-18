from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def open_player_page(driver, player_page_url):
    """
    Open the given player page on Rotowire
    
    :param driver: Selenium WebDriver object
    :param player_page_url: URL for the page whose player info is to be opened
    """
    driver.get(player_page_url)

def scroll_to_game_log(driver):
    """
    Scroll to the player's game log

    :param driver: Selenium WebDriver object
    """
    game_log = driver.find_element_by_id('gamelog-2020-stats')
    driver.execute_script("arguments[0].scrollIntoView();", game_log)

def use_dk_point_system(driver):
    """
    Change the game log to show the player's fantasy points using the DraftKings system

    :param driver: Selenium WebDriver object
    """
    dk_point_tab = driver.find_element_by_xpath("//div[@data-name='DraftKings']")
    dk_point_tab.click()

def get_dk_point_history(driver):
    """
    Get the player's DraftKings fantasy points for the player's last 15 games (includes DNPs)

    :param driver: Selenium WebDriver object
    """
    dk_point_history = [float(element.text) for element in driver.find_elements_by_xpath("//div[@id='gamelog-2020-stats']//div[@column=3]/div[not(contains(@class, 'p-page__gamelog-dnp'))][position()<16]")]
    return dk_point_history

def get_recently_injured(driver):
    """
    Get whether if the player was injured the last team game

    :param driver: Selenium WebDriver object
    :returns: True if the player was injured, False if not
    """
    last_game_minutes_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='gamelog-2020-stats']//div[@column=6]/div")))
    if last_game_minutes_element.text == 'DNP':
        return False
    return True
