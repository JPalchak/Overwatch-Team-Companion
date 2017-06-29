class Statistics:
    def __init__(self, debug_mode):
        self.debug_mode = debug_mode
        self.snapshots = []

    def add_snapshot(self, heroes, current_map, map_side, objective_progress):
        # TODO need game time
        self.snapshots.append(SnapShot(heroes, current_map, map_side, objective_progress))

    def submit_stats(self, game_end):
        if self.snapshots is not None:
            print(game_end)


class SnapShot:
    def __init__(self, heroes, current_map, map_side, objective_progress):
        self.heroes = heroes
        self.current_map = current_map
        self.map_side = map_side
        self.objective_progress = objective_progress
        print(heroes)
        print(current_map)
        print(map_side)
        print(objective_progress)


