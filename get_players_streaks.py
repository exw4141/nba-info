from selenium import webdriver
from sites import rotowire_lineups as lineups
from sites import rotowire_lineup_optimizer as lineup_optimizer
import sites.rotowire_player_page as player_page

from operator import attrgetter

import time

class Player:

    def __init__(self, name, salary, projected_points, num_fire_games, recent_streak, streaks):
        self._name = name
        self._salary = salary
        self._projected_points = projected_points
        self._num_fire_games = num_fire_games
        self._recent_streak = recent_streak
        self._streaks = streaks

    @property
    def name(self):
        return self._name

    @property
    def salary(self):
        return self._salary

    @property
    def projected_points(self):
        return self._projected_points

    @property
    def num_fire_games(self):
        return self._num_fire_games

    @property
    def recent_streak(self):
        return self._recent_streak

    @property
    def streaks(self):
        return self._streaks

    def __str__(self):
        return "{}, {}, {} games on fire, {} game streak".format(self._name, self._projected_points, self._num_fire_games, self._recent_streak)

    def __repr__(self):
        return self._name
        # return "{}, {}, {} games on fire, {} game streak".format(self._name, self._projected_points, self._num_fire_games, self._recent_streak)

def get_player_dk_points(driver, player_links):
    """
    Get DK points of the last 15 games for each player playing today
    :param driver: Selenium WebDriver object
    :param player_links: List of Selenium WebElements corresponding to links of players who have a game today
    :returns: A dictionary of players with player name being the key and a list of their DraftKings point totals over the last 15 games as the value 
    """
    player_dk_point_history = player_links
    for player_name in player_dk_point_history.keys():
        print(player_name)

        link = player_dk_point_history[player_name]
        driver.get(link)
        player_page.scroll_to_game_log(driver)
        player_page.use_dk_point_system(driver)
        time.sleep(4.5)
        dk_point_history = player_page.get_dk_point_history(driver)
        player_dk_point_history[player_name] = dk_point_history
        print(dk_point_history)
    return player_dk_point_history

def get_player_salary_and_points(driver, player_name):
    """
    Retrieve a player's salary and projected points
    :param driver: Selenium WebDriver object
    :param player_name: Name of the player to get salary and projected point total for
    :returns: The salary and projected point total of the player with the given player name
    """
    lineup_optimizer.search_player(driver, player_name)

    player_salaries = lineup_optimizer.get_player_salaries(driver)
    if len(player_salaries) == 0:
        lineup_optimizer.clear_search_input(driver)
        return -1, -1

    player_salary = player_salaries[0]
    player_salary = float(player_salary[1:])
    player_proj_points = (player_salary / 1000) * 5
    return player_salary, player_proj_points

def get_recent_streak(driver, on_fire, dk_point_history):
    """
    Get players recent fire or non-fire (neutral or cold) streak
    :param driver: Selenium WebDriver object
    :param on_fire: Boolean for whether the player is on a hot streak or cold streak
    :param dk_point_history: List of DraftKings point totals for a player
    :returns: An integer resembling a player's recent streak of games where the player has been consecutively hot or cold
    """
    recent_streak = 0
    if on_fire:
        for dk_points in dk_point_history:
            if dk_points >= player_proj_points + 4.5:
                recent_streak += 1
            else:
                break
    else:
        for dk_points in dk_point_history:
            if dk_points < player_proj_points + 4.5:
                recent_streak += 1
            else:
                break
    return recent_streak

def process_dk_point_history(driver, on_fire, dk_point_history):
    """
    Count number of games where the player was on fire and calculate their fire streaks
    :param driver: Selenium WebDriver object
    :param on_fire: Boolean for whether the player is on a hot streak or cold streak
    :param dk_point_history: List of DraftKings point totals for a player
    :returns: A integer resembling the number of games in which a player has been on fire and a list of their hot streaks (if on fire) or cold streaks (if not on fire)
    """
    num_fire_games = 0
    player_streaks = []
    current_streak = 0
    if on_fire:
        for dk_points in dk_point_history:
            if dk_points >= player_proj_points + 4.5:
                current_streak += 1
                num_fire_games += 1
            else:
                if current_streak > 0:
                    player_streaks.append(current_streak)
                    current_streak = 0
        if current_streak > 0 and current_streak > recent_streak:
            player_streaks.append(current_streak)
    else:
        for dk_points in dk_point_history:
            if dk_points < player_proj_points + 4.5:
                current_streak += 1
            else:
                if current_streak > 0:
                    player_streaks.append(current_streak)
                    current_streak = 0
                num_fire_games += 1
        # Not sure whether to add a streak that is cut off
        if current_streak > 0 and current_streak != recent_streak:
            player_streaks.append(current_streak)
    return num_fire_games, player_streaks

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()

    lineups.open_rotowire_lineups(driver)
    rotowire_player_links = lineups.get_player_links(driver)

    dk_point_histories = get_player_dk_points(driver, rotowire_player_links)

    lineup_optimizer.open_rotowire_lineup_optimizer(driver)

    fire_players = []
    cold_players = []
    all_players = []
    for player_name in dk_point_histories.keys():
        player_salary, player_proj_points = get_player_salary_and_points(driver, player_name)
        if player_salary == -1:
            continue

        # Determine if the player was fire last game or not
        dk_point_history = dk_point_histories[player_name]
        if len(dk_point_history) > 0:
            if dk_point_history[0] >= player_proj_points + 4.5:
                on_fire = True
            else:
                on_fire = False
        else:
            on_fire = False

        recent_streak = get_recent_streak(driver, on_fire, dk_point_history)
        num_fire_games, player_streaks = process_dk_point_history(driver, on_fire, dk_point_history)

        if on_fire:
            output_string = f"{player_name}\n" \
                            f"Number of fire games within the last 15 games: {num_fire_games}\n" \
                            f"Recent fire streak: {recent_streak}\n" \
                            f"Previous fire streaks: {player_streaks[1:]}\n"
        else:
            output_string = f"{player_name}\n" \
                            f"Number of fire games within the last 15 games: {num_fire_games}\n" \
                            f"Recent non-fire streak: {recent_streak}\n" \
                            f"Previous non-fire streaks: {player_streaks[1:]}\n"
        print(output_string)

        player = Player(player_name, player_salary, player_proj_points, num_fire_games, recent_streak, player_streaks[1:])
        if on_fire:
            fire_players.append(player)
        else:
            cold_players.append(player)
        all_players.append(player)

        lineup_optimizer.clear_search_input(driver)

    fire_players.sort(key=attrgetter('recent_streak', 'num_fire_games', 'projected_points'), reverse=True)
    print('Fire players: ', fire_players, sep='\n')
    print()

    cold_players.sort(key=attrgetter('recent_streak', 'num_fire_games', 'projected_points'), reverse=True)
    print('Cold players: ', cold_players, sep='\n')
    print()

    all_players.sort(key=attrgetter('num_fire_games', 'recent_streak', 'projected_points'), reverse=True)
    print('All players:', all_players, sep='\n')

    time.sleep(3)
    driver.close()
