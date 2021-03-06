from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def open_rotowire_lineup_optimizer(driver):
    """
    Open the RotoWire Lineup Optimizer page

    :param driver: Selenium WebDriver object
    """
    driver.get('https://www.rotowire.com/daily/nba/optimizer.php?site=DraftKings')

def search_player(driver, player_name):
    """
    Searches for a player within the site's player table

    :param driver: Selenium WebDriver object
    """
    current_url = driver.current_url

    if current_url.startswith('https://www.rotowire.com/daily/nba/optimizer.php'):
        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'table-ufilters__search'))
        )
        search_input.send_keys(player_name)
    else:
        print("Wrong webpage in use. Unable to search for players.")

def clear_search_input(driver):
    """
    Clear the player name textbox

    :param driver: Selenium WebDriver object
    """
    current_url = driver.current_url

    if current_url.startswith('https://www.rotowire.com/daily/nba/optimizer.php'):
        clear_search_input_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'table-ufilters__clear'))
        )
        clear_search_input_button.click()
    else:
        print("Wrong webpage in use. Unable to clear player search.")

def sort_players_by_value(driver):
    """
    Sort players in the table by projected value. Assumes the players are not sorted by value yet.

    :param driver: Selenium WebDriver object
    """
    current_url = driver.current_url

    if current_url.startswith('https://www.rotowire.com/daily/nba/optimizer.php'):
        fantasy_point_col_header = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//td[@column='13']/div"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", fantasy_point_col_header)
        fantasy_point_col_header.click()
        fantasy_point_col_header.click()

        value_col_header = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//td[@column='14']/div"))
        )
        value_col_header.click()
    else:
        print("Wrong webpage in use. Unable to sort players by value.")

def sort_players_by_salary(driver):
    """
    Sorts players in the table by their salaries

    :param driver: Selenium WebDriver object
    """
    current_url = driver.current_url

    if current_url.startswith('https://www.rotowire.com/daily/nba/optimizer.php'):
        salary_col_header = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//td[@column='12']/div"))
        )
        salary_col_header.click()
    else:
        print("Wrong webpage in use. Unable to sort players by salary.")

def get_player_info(driver):
    """
    Gets various info of players playing on today's daily fantasy basketball slate

    :param driver: Selenium WebDriver object
    :returns: A tuple of lists containing player names, their positions, salaries, and projected values
    """
    player_names = get_player_names(driver)
    player_positions = get_player_positions(driver)
    player_status = get_player_status(driver)
    player_salaries = get_player_salaries(driver)
    player_values = get_player_proj_values(driver)
    return player_names, player_positions, player_status, player_salaries, player_values

def get_player_names(driver):
    """
    Get the names of the players playing on today's daily fantasy basketball slate

    :param driver: Selenium WebDriver object
    :returns: A list containing the names of players playing today
    """
    current_url = driver.current_url

    if current_url.startswith('https://www.rotowire.com/daily/nba/optimizer.php'):
        player_names = driver.find_elements_by_xpath("//div[contains(@class, 'name')]/div/span[contains(@data-name, ' ')]")
        for i in range(0, len(player_names)):
            player_names[i] = player_names[i].get_attribute('data-name')
        return player_names
    else:
        print("Wrong webpage in use. Unable to get names of players.")

def get_player_positions(driver):
    """
    Get the positions of the players playing on today's daily fantasy basketball slate

    :param driver: Selenium WebDriver object
    :returns: A list containing the positions of players playing today
    """  
    current_url = driver.current_url

    if current_url.startswith('https://www.rotowire.com/daily/nba/optimizer.php'):
        player_positions = driver.find_elements_by_xpath("//div[contains(@class, 'position')]/div[@role='gridcell']")
        for i in range(0, len(player_positions)):
            player_positions[i] = player_positions[i].text
        return player_positions
    else:
        print("Wrong webpage in use. Unable to get positions of players.")

def get_player_status(driver):
    """
    Get the status of the players playing on today's daily fantasy basketball slate

    :param driver: Selenium WebDriver object
    :returns: A list containing the status of players playing today
    """
    current_url = driver.current_url

    if current_url.startswith('https://www.rotowire.com/daily/nba/optimizer.php'):
        player_status = driver.find_elements_by_xpath("//div[contains(@class, 'lineup_status')]/div[@role='gridcell']")
        for i in range(0, len(player_status)):
            player_status[i] = player_status[i].text
        return player_status
    else:
        print("Wrong webpage in use. Unable to get status of players.")

def get_player_salaries(driver):
    """
    Get the salaries of the players playing on today's daily fantasy basketball slate

    :param driver: Selenium WebDriver object
    :returns: A list containing the salaries of players playing today
    """
    current_url = driver.current_url

    if current_url.startswith('https://www.rotowire.com/daily/nba/optimizer.php'):
        player_salaries = driver.find_elements_by_xpath("//div[contains(@class, 'salary')]/div[@role='gridcell']/input")
        for i in range(0, len(player_salaries)):
            player_salaries[i] = player_salaries[i].get_attribute('value')
        return player_salaries
    else:
        print("Wrong webpage in use. Unable to get salaries of players.")

def get_player_proj_values(driver):
    """
    Get the projected values of the players playing on today's daily fantasy basketball slate

    :param driver: Selenium WebDriver object
    :returns: A list containing the projected values of players playing today
    """
    current_url = driver.current_url

    if current_url.startswith('https://www.rotowire.com/daily/nba/optimizer.php'):
        player_values = driver.find_elements_by_xpath("//div[contains(@class, 'value')]/div[@role='gridcell']")
        for i in range(0, len(player_values)):
            player_values[i] = player_values[i].text
        return player_values
    else:
        print("Wrong webpage in use. Unable to get projected salaries of players.")

def filter_by_position(driver, position):
    """
    Filter the player table by position

    :param driver: Selenium WebDriver object
    """
    if position == 'UTIL':
        filter_xpath = "//div[text()='All']"
    else:
        filter_xpath = "//div[text()='{}']".format(position)

    player_filter = driver.find_element_by_xpath(filter_xpath)
    player_filter.click()

def get_player_table_scrollbar(driver):
    """
    Get the player table's scrollbar element

    :param driver: Selenium WebDriver object
    :returns: The player table's scrollbar element
    """
    player_table_scrollbar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'players-table')]/div[contains(@class, 'webix_vscroll_y')]"))
    )
    return player_table_scrollbar
