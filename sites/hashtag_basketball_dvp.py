from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time # TODO remove after implementing necesary functions

def open_dvp_page(driver):
    """
    Open Hashtag Basketball's Defense vs. Position page

    :param driver: Selenium WebDriver object
    """
    driver.get('https://hashtagbasketball.com/nba-defense-vs-position')

def change_time_range_filter(driver, time_range=1):
    """
    Change time range of games to use for defense vs. position statistics.

    :param driver: Selenium WebDriver object
    :param time_range: Time range of games to use. Use 1 for the whole season (default), 7 for the past 7 days, 14 for the past 14 days, and 30 for the past 30 days.
    :raises TypeError: Error raised if time_range is not a integer
    :raises ValueError: Error raised if time_range is not 1, 7, 14, or 30.
    """
    if not isinstance(time_range, int):
        raise TypeError("time_range parameter requires a value of type 'int'")

    time_range_dropdown = Select(driver.find_element_by_xpath("//select[contains(@name, 'DDDURATION')]"))

    if time_range == 1:
        time_range_dropdown.select_by_value('1')
    elif time_range == 7:
        time_range_dropdown.select_by_value('7')
    elif time_range == 14:
        time_range_dropdown.select_by_value('14')
    elif time_range == 30:
        time_range_dropdown.select_by_value('30')
    else:
        raise ValueError('Invalid time range given to function. Can only use statistics for games from the whole season or the past 7 days, 14 days, or 30 days')

    # Give time for the statistics table to reload
    time.sleep(2)

def get_selected_time_range(driver):
    """
    Get the currently selected time range used for defense vs. position statistics

    :param driver: Selenium WebDriver object
    :returns: The currently selected time range. A value of "1" means that the whole season is being used for statistics. 
    """
    time_range_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[contains(@name, 'DDDURATION')]"))
    )
    time_range_dropdown = Select(time_range_dropdown)
    return time_range_dropdown.first_selected_option.get_attribute('value')

def change_position_filter(driver, position='ALL'):
    """
    Filter defense vs. position statistics by player position

    :param driver: Selenium WebDriver object
    :param position: Player position to filter by. Use "PG" for point guards, "SG" for shooting guards, "SF" for small forwards, "PF" for power forwards, or "C" for centers
    """
    if not isinstance(position, str):
        raise TypeError("position parameter requires a value of type 'str'")

    position_dropdown = Select(driver.find_element_by_xpath("//select[contains(@id, 'DropDownList1')]"))
    
    position = position.upper()
    if position == 'ALL':
        position_dropdown.select_by_value('All positions')
    elif position == 'PG':
        position_dropdown.select_by_value('PG')
    elif position == 'SG':
        position_dropdown.select_by_value('SG')
    elif position== 'SF':
        position_dropdown.select_by_value('SF')
    elif position == 'PF':
        position_dropdown.select_by_value('PF')
    elif position == 'C':
        position_dropdown.select_by_value('C')
    else:
        raise ValueError('Invalid position given to function. Can only be PG (point guard), SG (shooting guard), SF (small forward), PF (power forward), or C (center).')

    # Give time for the statistics table to reload
    time.sleep(2)

def get_selected_position(driver):
    """
    Get the current player position used for filtering stats

    :param driver: Selenium WebDriver object
    :returns: The currently selected player position. Returns "All positions" statistics are not being filtered by player position. 
    """
    position_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[contains(@id, 'DropDownList1')]"))
    )
    position_dropdown = Select(position_dropdown)
    return position_dropdown.first_selected_option.text

def sort_defenses_by_points(driver):
    """
    Sorts defenses in the table with all teams by points

    :param driver: Selenium WebDriver object
    """
    sort_by_points_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()='POSITION DATA']/following-sibling::div[@class='table-responsive']//table[contains(@id, 'GridView1')]//a[text()='Sort: PTS']"))
    )
    sort_by_points_element.click()

    # Give time for the statistics table to reload
    time.sleep(2)

def get_defense_papg(driver):
    """
    Gets the points allowed per game stat for all teams. Currently assumes that the defenses are being filtered by player position

    :param driver: Selenium WebDriver object
    :returns: A list of tuples where each tuple contains a team's abbreviation and the team's points allowed per game statistic vs. the currently selected player position
    """    
    team_label_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@id, 'ContentPlaceHolder1_GridView1_Label1') and not(contains(@id, 'Label10'))]"))
    )
    papg_label_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@id, 'ContentPlaceHolder1_GridView1_Label2')]"))
    )

    teams_points_allowed_per_game_stats = []
    for i in range(0, len(team_label_elements)):
        team = team_label_elements[i].text
        stat = papg_label_elements[i].text

        teams_points_allowed_per_game_stats.append((team, float(stat)))
    return teams_points_allowed_per_game_stats

# Main below is just for testing purposes
if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    open_dvp_page(driver)
    change_time_range_filter(driver, 14)
    print(get_selected_time_range(driver))
    change_position_filter(driver, 'C')
    print(get_selected_position(driver))
    sort_defenses_by_points(driver)
    print(get_defense_papg(driver))
    
    time.sleep(5)
    driver.close()
