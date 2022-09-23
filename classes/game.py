import re
import time
import pickle
import random
from selenium import webdriver
from selenium.webdriver.common.by import By


class Game():
    def __init__(self):
        self.driver = webdriver.Chrome(
            executable_path='web_driver/chromedriver.exe')

    def get_web(self, link):
        time.sleep(random.randint(10, 25))
        
        return self.driver.get(link)

    def get_cookies(self):
        return pickle.dump(
            self.driver.get_cookies(), open("cookies/ceroacero_cookies_login.pkl", "wb"))

    def add_cookies(self):
        cookies = pickle.load(
            open("cookies/ceroacero_cookies_login.pkl", "rb"))

        for cookie in cookies:
            self.driver.add_cookie(cookie)

        self.driver.refresh()

    def games_links(self):

        links = self.driver.find_elements(By.CLASS_NAME, "result > a")

        links = [link.get_attribute("href") for link in links]

        return links

    def dates_games(self):

        dates = self.driver.find_element(By.CLASS_NAME, "box_container")
        dates = list(map(str.strip, dates.text.split("\n")))

        # Obtener fecha del Partido
        dates_games = []
        # Obtener Resultados de los Partidos
        for date_game in dates:
            if bool(re.match(r"[\d][\d]", date_game)):
                date_game = date_game[:5]
                date_game = date_game[6:]

                dates_games.append(date_game)
            else:
                dates_games.append(date_game)

        return dates_games

    def get_jornadas(self, year=2020):
        if year==2021:
            return len(self.driver.find_elements(
                By.XPATH, '//*[@id="page_submenu"]/ul/li[3]/form/div[2]/label/select/option'))-1

        return len(self.driver.find_elements(
                By.XPATH, '//*[@id="page_submenu"]/ul/li[1]/form/div[2]/label/select/option'))-1

    def game_stats(self):

        stats = self.driver.find_element(
            By.XPATH, '//*[@id="page_rightbar"]/div[3]/div/div[2]')
        all_stats = stats.text.split('\n')
        all_stats = [stats.strip(' ') for stats in all_stats]
        all_stats = [all_stats[i:i+3] for i in range(0, len(all_stats), 3)]

        return all_stats
