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

def change_time_range(driver, time_range=1):
    """
    Change time range of games to use for defense vs. position statistics.

    :param driver: Selenium WebDriver object
    :param time_range: Time range of games to use. Use 1 for the whole season, 7 for the past 7 days, 14 for the past 14 days, and 30 for the past 30 days.
    :raises ValueError: Error raised if time_range is not 1, 7, 14, or 30.
    """
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

def sort_all_defenses_by_points(driver):
    """
    Sorts defenses in the table with all teams by points

    :param driver: Selenium WebDriver object
    """
    sort_by_points_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()='POSITION DATA']/following-sibling::div[@class='table-responsive']//table[contains(@id, 'GridView1')]//a[text()='Sort: PTS']"))
    )
    sort_by_points_element.click()

# Main below is just for testing purposes
if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    open_dvp_page(driver)
    change_time_range(driver, 14)

    sort_all_defenses_by_points(driver)
    
    time.sleep(5)
    driver.close()
