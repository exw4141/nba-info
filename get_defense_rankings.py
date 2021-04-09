from selenium import webdriver
import sites.hashtag_basketball_dvp as dvp

import time

class TeamDefense:

    def __init__(self, team):
        self._team = team
        self._pg_papg = {1: None, 7: None, 14: None, 30: None}
        self._sg_papg = {1: None, 7: None, 14: None, 30: None}
        self._sf_papg = {1: None, 7: None, 14: None, 30: None}
        self._pf_papg = {1: None, 7: None, 14: None, 30: None}
        self._c_papg = {1: None, 7: None, 14: None, 30: None}

        self._pg_ranking = {1: None, 7: None, 14: None, 30: None}
        self._sg_ranking = {1: None, 7: None, 14: None, 30: None}
        self._sf_ranking = {1: None, 7: None, 14: None, 30: None}
        self._pf_ranking = {1: None, 7: None, 14: None, 30: None}
        self._c_ranking = {1: None, 7: None, 14: None, 30: None}

    def add_papg(self, time_range, position, papg):
        """
        Records the team's points allowed per game stat at the given position for the given time range
        :param time_range: The time range for which the given points allowed per game stat is being recorded for
        :param position: The position for which the given points allowed per game stat is being recorded for
        :param papg: Number of points allowed per game 
        :raises ValueError: Raised if the player position provided is not valid
        """
        if position == 'PG':
            self._pg_papg[time_range] = papg
        elif position == 'SG':
            self._sg_papg[time_range] = papg
        elif position == 'SF':
            self._sf_papg[time_range] = papg
        elif position == 'PF':
            self._pf_papg[time_range] = papg
        elif position == 'C':
            self._c_papg[time_range] = papg
        else:
            raise ValueError('Invalid position given to function. Can only be PG (point guard), SG (shooting guard), SF (small forward), PF (power forward), or C (center).')

    def set_ranking(self, time_range, position, ranking):
        """
        Records the team's defensive ranking (based on points allowed per game) at the given position for the given time range
        :param time_range: The time range for which the ranking is being recorded for
        :param position: The position for which the ranking is being recorded for
        :param ranking: Team's points allowed per game ranking compared to other teams
        :raises ValueError: Raised if the player position provided is not valid
        """
        if position == 'PG':
            self._pg_ranking[time_range] = ranking
        elif position == 'SG':
            self._sg_ranking[time_range] = ranking
        elif position == 'SF':
            self._sf_ranking[time_range] = ranking
        elif position == 'PF':
            self._pf_ranking[time_range] = ranking
        elif position == 'C':
            self._c_ranking[time_range] = ranking
        else:
            raise ValueError('Invalid position given to function. Can only be PG (point guard), SG (shooting guard), SF (small forward), PF (power forward), or C (center).')

    def create_defense_papg_summary(self):
        """
        Formats output to display each team's points allowed per game over different time ranges
        :returns: A string that displays all teams's points allowed per game
        """
        stat_summary = f"{self._team}\n"
        positions = ['PG', 'SG', 'SF', 'PF', 'C']
        for position in positions:
            stat_summary += "{}:\n".format(position)
            if position == 'PG':
                for time_range in self._pg_papg:
                    papg_stat = str(self._pg_papg[time_range])
                    stat_summary += f"{time_range}: {papg_stat}\n"
            elif position == 'SG':
                for time_range in self._sg_papg:
                    papg_stat = str(self._sg_papg[time_range])
                    stat_summary += f"{time_range}: {papg_stat}\n"
            elif position == 'SF':
                for time_range in self._sf_papg:
                    papg_stat = str(self._sf_papg[time_range])
                    stat_summary += f"{time_range}: {papg_stat}\n"
            elif position == 'PF':
                for time_range in self._pf_papg:
                    papg_stat = str(self._pf_papg[time_range])
                    stat_summary += f"{time_range}: {papg_stat}\n"
            elif position == 'C':
                for time_range in self._c_papg:
                    papg_stat = str(self._c_papg[time_range])
                    stat_summary += f"{time_range}: {papg_stat}\n"
            stat_summary += '\n'
        return stat_summary

    def create_defense_ranking_summary(self):
        """
        Formats output to display each team's defensive ranking over different time ranges
        :returns: A string that displays all team's defensive rankings
        """ 
        ranking_summary = f"{self._team}\n"
        positions = ['PG', 'SG', 'SF', 'PF', 'C']
        for position in positions:
            ranking_summary += "{}:\n".format(position)
            if position == 'PG':
                for time_range in self._pg_ranking:
                    ranking = str(self._pg_ranking[time_range])
                    ranking_summary += f"{time_range}: {ranking}\n"
            elif position == 'SG':
                for time_range in self._sg_ranking:
                    ranking = str(self._sg_ranking[time_range])
                    ranking_summary += f"{time_range}: {ranking}\n"
            elif position == 'SF':
                for time_range in self._sf_ranking:
                    ranking = str(self._sf_ranking[time_range])
                    ranking_summary += f"{time_range}: {ranking}\n"
            elif position == 'PF':
                for time_range in self._pf_ranking:
                    ranking = str(self._pf_ranking[time_range])
                    ranking_summary += f"{time_range}: {ranking}\n"
            elif position == 'C':
                for time_range in self._c_ranking:
                    ranking = str(self._c_ranking[time_range])
                    ranking_summary += f"{time_range}: {ranking}\n"
            ranking_summary += '\n'
        return ranking_summary

    def __str__(self):
        return self.create_defense_ranking_summary()

    def __repr__(self):
        return self.create_defense_ranking_summary()

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()

    dvp.open_dvp_page(driver)
    dvp.sort_defenses_by_points(driver)
    
    team_defenses = {}
    positions = ['PG', 'SG', 'SF', 'PF', 'C']
    time_ranges = [1, 7, 14, 30]
    for position in positions:
        dvp.change_position_filter(driver, position)

        for time_range in time_ranges:
            dvp.change_time_range_filter(driver, time_range)
            defense_papgs = dvp.get_defense_papg(driver)
            
            last_papg = defense_papgs[0][1]
            cur_ranking = 1
            team_number = 1
            for defense in defense_papgs:
                team = defense[0]
                papg = defense[1]

                if team not in team_defenses:
                    team_defenses[team] = TeamDefense(team)

                team_defenses[team].add_papg(time_range, position, papg)
                if papg == last_papg:
                    team_defenses[team].set_ranking(time_range, position, cur_ranking)
                else:
                    cur_ranking = team_number
                    team_defenses[team].set_ranking(time_range, position, cur_ranking)
                
                team_number += 1
                last_papg = papg
    
    for team in team_defenses:
        print(team_defenses[team])
    
    time.sleep(3)
    driver.close()
