from audioop import add
import re
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By


class Game():
    def __init__(self):
        self.driver = webdriver.Chrome(
            executable_path='web_driver/chromedriver.exe')

    def get_web(self, link):
        return self.driver.get(link)

    def add_cookies(self):
        cookies = pickle.load(
            open("cookies/ceroacero_cookies.pkl", "rb"))

        for cookie in cookies:
            self.driver.add_cookie(cookie)

        self.driver.refresh()

    def games_links(self):

        links = self.driver.find_elements(By.CLASS_NAME, "result > a")
        links = links[:len(links)//2]
        links = [link.get_attribute("href") for link in links]

        return links

    def dates_games(self):

        dates = self.driver.find_element(By.CLASS_NAME, "box_container")
        dates = list(map(str.strip, dates.text.split("\n")))

        # Obtener fecha del Partido
        dates_games = []
        for game in dates:
            if bool(re.match(r"[\d][\d]", game)):
                date_game = game[:5]
                game = game[6:]

                dates_games.append(date_game)
            else:
                dates_games.append(date_game)

        return dates_games

    def get_jornadas(self):

        return len(self.driver.find_elements(
            By.XPATH, '//*[@id="page_submenu"]/ul/li[1]/form/div[2]/label/select/option'))-1

    def game_stats(self):

        stats = self.driver.find_element(
            By.XPATH, '//*[@id="page_rightbar"]/div[3]/div/div[2]')
        all_stats = stats.text.split('\n')
        all_stats = [stats.strip(' ') for stats in all_stats]
        all_stats = [all_stats[i:i+3] for i in range(0, len(all_stats), 3)]

        return all_stats
