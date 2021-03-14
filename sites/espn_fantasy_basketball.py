from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time

def open_espn(driver):
    driver.get('https://fantasy.espn.com/basketball/players/add?leagueId=184988581')

def show_all_players(driver):
    current_url = driver.current_url

    if current_url.startswith('https://fantasy.espn.com/basketball/players/add?leagueId='):
        player_availability_filter_all = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//select[@id='filterStatus']/option[@value='ALL']"))
        )
        player_availability_filter_all.click()
    else:
        print("Wrong webpage in use. Unable to show all players.")

def use_last15_stats(driver):
    """
    """
    current_url = driver.current_url

    if current_url.startswith('https://fantasy.espn.com/basketball/players/add?leagueId='):
        stats_dropdown_last15_option = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//select[@id='filterStat']/option[@value='last15']"))
        )
        stats_dropdown_last15_option.click()
    else:
        print("Wrong webpage in use. Unable to use stats for last 15 games.")

def search_player(driver, player_name):
    """
    """
    current_url = driver.current_url

    if current_url.startswith('https://fantasy.espn.com/basketball/players/add?leagueId='):
        player_search = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, player--search)]/input[@placeholder='Player Name']"))
        )
        player_search.send_keys(player_name)

        search_result_xpath = "//div[@class='player--search--matches']/button[@data-player-search-playername='{}']".format(player_name)
        search_result = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, search_result_xpath))
        )

        # Wait for search results
        time.sleep(0.5)
        search_result.click()
        player_search.clear()
    else:
        print("Wrong webpage in use. Unable to search for a player.")

def sort_players_by_minutes(driver):
    current_url = driver.current_url

    if current_url.startswith('https://fantasy.espn.com/basketball/players/add?leagueId='):
        minute_column_header = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@title='Minutes' and contains(@class, 'header')]"))
        )
        minute_column_header.click()
    else:
        print("Wrong webpage in use. Unable to sort players by minutes.")

def get_all_player_names(driver):
    current_url = driver.current_url

    if current_url.startswith('https://fantasy.espn.com/basketball/players/add?leagueId='):
        player_name_elements = driver.find_elements_by_xpath("//div[contains(@class, 'player-column__athlete')]")
        for i in range(0, len(player_name_elements)):
            player_name_elements[i] = player_name_elements[i].get_attribute('title')
        return player_name_elements
    else:
        print("Wrong webpage in use. Unable to use find names of all players.")

def get_all_player_steals(driver):
    current_url = driver.current_url

    if current_url.startswith('https://fantasy.espn.com/basketball/players/add?leagueId='):
        steal_elements = driver.find_elements_by_xpath("//div[@title='Steals' and not(contains(@class, 'header'))]")
        for i in range(0, len(steal_elements)):
            steal_elements[i] = steal_elements[i].text
        return steal_elements
    else:
        print("Wrong webpage in use. Unable to use find steals statistic of all players.")

def get_player_steals(driver):
    current_url = driver.current_url

    if current_url.startswith('https://fantasy.espn.com/basketball/players/add?leagueId='):
        player_steals = driver.find_elements_by_xpath("//div[@title='Steals' and not(contains(@class, 'header'))]")

        # Would function incorrectly if players have the same name
        if len(player_steals) > 1:
            print("Multiple players have been found. Make sure you have searched for a specific player.")
            return

        time.sleep(0.5)
        return player_steals[0].text
    else:
        print("Wrong webpage in use. Unable to use find steals statistic.")

def get_all_player_blocks(driver):
    current_url = driver.current_url

    if current_url.startswith('https://fantasy.espn.com/basketball/players/add?leagueId='):
        block_elements = driver.find_elements_by_xpath("//div[@title='Blocks' and not(contains(@class, 'header'))]")
        for i in range(0, len(block_elements)):
            block_elements[i] = block_elements[i].text
        return block_elements
    else:
        print("Wrong webpage in use. Unable to use find blocks statistic of all players.")

def get_player_blocks(driver):
    current_url = driver.current_url

    if current_url.startswith('https://fantasy.espn.com/basketball/players/add?leagueId='):
        player_blocks = driver.find_elements_by_xpath("//div[@title='Blocks' and not(contains(@class, 'header'))]")
        
        # Would function incorrectly if players have the same name
        if len(player_blocks) > 1:
            print("Multiple players have been found. Make sure you have searched for a specific player.")
            return

        time.sleep(0.5)
        return player_blocks[0].text
    else:
        print("Wrong webpage in use. Unable to use find blocks statistic.")

def go_to_next_page(driver):
    current_url = driver.current_url

    if current_url.startswith('https://fantasy.espn.com/basketball/players/add?leagueId='):
        next_page_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(@class, 'Pagination__Button--next')]"))
        )
        next_page_button.click()
    else:
        print("Wrong webpage in use. Unable to go to the next page of players.")
