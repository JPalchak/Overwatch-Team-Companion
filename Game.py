from PIL import ImageGrab
import numpy as np
from datetime import datetime
import subprocess as sp
import copy
import time

from Statistics import Statistics
from AllHeroes import AllHeroes
from MapInfo import MapInfo
from TimeInfo import TimeInfo


class Game:
    def __init__(self, game_version, debug_mode):
        self.game_version = game_version
        self.debugMode = debug_mode
        self.heroes = AllHeroes(game_version, debug_mode)
        self.map = MapInfo(game_version, debug_mode)
        self.statistics = None
        self.gameTime = TimeInfo(game_version, debug_mode)
        self.game_over = True

    def main(self, broadcaster):
        start_time = time.time()

        sleep_time = None
        current_time = datetime.now()
        current_time_string = datetime.strftime(current_time, "%m-%d-%y %H-%M-%S")

        screen_img_array = self.get_screen()
        current_view = self.map.main(screen_img_array, current_time_string)
        if current_view:
            # TODO uncomment
            # sp.call('cls', shell=True)
            print(self.map.get_current_map())
            print(current_view)

            # check if map or side changed
            map_changed = self.map.mapChange
            if current_view == "Hero Select":
                side_changed = self.map.identify_side(screen_img_array)
            else:
                side_changed = False

            self.heroes.main(screen_img_array, current_time_string, current_view)

            if map_changed or side_changed:
                self.map.broadcast_options(broadcaster)
                self.map.reset_objective_progress()
                self.game_over = False
            if map_changed and current_view == "Hero Select":
                print("ClearEnemyHeroes")
                self.heroes.clear_enemy_heroes(broadcaster)
                self.statistics = Statistics(self.debugMode)
            else:  # because clear_enemy_heroes already broadcasts heroes
                heroes_changed = self.heroes.check_for_change()
                if heroes_changed:
                    self.heroes.broadcast_heroes(broadcaster)

            if current_view == "Tab":
                sleep_time = 0.5
                self.map.identify_objective_progress(screen_img_array, current_view=current_view)
                self.gameTime.main(screen_img_array, current_time_string)
            elif current_view == "Hero Select":
                sleep_time = 1

        else:
            sleep_time = 0
            if self.game_over is False:
                self.map.identify_objective_progress(screen_img_array)

        # game stats tracking
        if self.statistics is not None:
            if self.map.objectiveProgress["gameOver"]:
                self.game_over = True
                print("Submit Stats and Clear")
                self.statistics.submit_stats(self.map.objectiveProgress["gameEnd"], current_time)
                self.statistics = None
                sleep_time = 10
                # TODO remove
                # self.map.reset_objective_progress()
            else:
                self.statistics.add_snapshot(self.heroes.heroesList, self.map.get_current_map(),
                                             self.map.currentMapSide, copy.deepcopy(self.map.get_objective_progress()),
                                             self.gameTime.get_verified_game_time(current_time), current_time)
        time_difference = time.time() - start_time
        if time_difference < 0.5:
            sleep_time = 0.5 - time_difference
        else:
            sleep_time = 0
        return sleep_time

    @staticmethod
    def get_screen():
        screen_img = ImageGrab.grab(bbox=None)
        return np.asarray(screen_img)
