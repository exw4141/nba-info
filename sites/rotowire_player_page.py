from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def open_player_page(driver, player_page_url):
    driver.get(player_page_url)

def scroll_to_game_log(driver):
    game_log = driver.find_element_by_id('gamelog-2020-stats')
    driver.execute_script("arguments[0].scrollIntoView();", game_log)

def use_dk_point_system(driver):
    dk_point_tab = driver.find_element_by_xpath("//div[@data-name='DraftKings']")
    dk_point_tab.click()

def get_dk_point_history(driver):
    dk_point_history = [float(element.text) for element in driver.find_elements_by_xpath("//div[@id='gamelog-2020-stats']//div[@column=3]/div[not(contains(@class, 'p-page__gamelog-dnp'))][position()<16]")]
    # print(dk_point_history)
    return dk_point_history

def get_recently_injured(driver):
    last_game_minutes_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='gamelog-2020-stats']//div[@column=6]/div")))
    if last_game_minutes_element.text == 'DNP':
        return False
    return True
