import re
import time
import pickle
import random
from classes.links import dummy_links
from selenium import webdriver
from selenium.webdriver.common.by import By


class Game():
    def __init__(self):
        self.driver = webdriver.Chrome(
            executable_path='web_driver/chromedriver.exe')

    def get_web(self, link):

        # self.driver.get(random.choice(dummy_links))
        time.sleep(random.randint(5, 15))

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

    def dates_games(self, jornada):

        # Partidos con fecha y resultado
        results = self.driver.find_element(By.CLASS_NAME, "box_container")
        results = list(map(str.strip, results.text.split("\n")))

        # Links de las estadisiticas de todos los partidos por jornada
        games_links = self.driver.find_elements(By.CLASS_NAME, "result > a")
        games_links = [link.get_attribute("href") for link in games_links]

        # Obtener Datos de los Partidos: Fecha - Equipo Local - Equipo Visitante - Goles Locales - Goles Visitante
        games_date = []
        for game, link in zip(results, games_links):
            if bool(re.match(r"[\d][\d]", game)):
                date_game = game[:5]
                game = game[6:]

                # Nombres de los equipos
                teams_score = game.split('-')
                if len(teams_score) < 2:
                    teams_score = game.split(' DA ')

                # print(teams_score)
                name_local = ' '.join(teams_score[0].split()[:-1])
                name_away = ' '.join(teams_score[1].split()[1:-1])

                # Resultados
                score_local = re.findall(r'\d+', teams_score[0])[0]
                score_away = re.findall(r'\d+', teams_score[1])[0]

                games_date.append([jornada, date_game, name_local,
                                   name_away, int(score_local), int(score_away), link])
            else:
                # Nombres de los equipos
                teams_score = game.split('-')
                if len(teams_score) < 2:
                    teams_score = game.replace(' DA ', ' 3-0 ').split('-')

                # print(teams_score)
                name_local = ' '.join(teams_score[0].split()[:-1])
                name_away = ' '.join(teams_score[1].split()[1:-1])

                # Resultados
                score_local = re.findall(r'\d+', teams_score[0])[0]
                score_away = re.findall(r'\d+', teams_score[1])[0]

                games_date.append([jornada, date_game, name_local,
                                   name_away, int(score_local), int(score_away), link])

        return games_date

    def get_jornadas(self, year=2020):
        if year == 2021:
            return len(self.driver.find_elements(
                By.XPATH, '//*[@id="page_submenu"]/ul/li[3]/form/div[2]/label/select/option'))-1

        return len(self.driver.find_elements(
            By.XPATH, '//*[@id="page_submenu"]/ul/li[1]/form/div[2]/label/select/option'))-1

    def game_stats(self):

        try:
            stats = self.driver.find_element(
                By.XPATH, '//*[@id="page_rightbar"]/div[3]/div/div[2]')

            all_stats = stats.text.split('\n')
            all_stats = [stats.strip(' ') for stats in all_stats]
            all_stats = {all_stats[i]: all_stats[i+1:i+3]
                         for i in range(0, len(all_stats), 3)}

            return all_stats

        except:

            all_stats = {}

            return all_stats
