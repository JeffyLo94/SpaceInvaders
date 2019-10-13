import json


class GameStats:

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings

        # init to get rid of pep8 warning
        self.ships_left = 0
        self.score = 0
        self.level = 0

        self.reset_stats()

        # Start game in an inactive state.
        self.is_game_active = False

        # High score should never be reset.
        self.high_score = 0

        self.aliens_start = None
        self.next_speed = None
        self.aliens_left = None
        self.high_scores_json = None
        self.high_scores_list = None
        self.init_high_scores()

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def init_high_scores(self):
        try:
            # print(self.ai_settings.high_score_datafile)
            with open(self.ai_settings.high_score_datafile, 'r') as file:
                self.high_scores_json = json.load(file)
                self.high_scores_list = sorted(self.high_scores_json, key=lambda k: k['score'], reverse=True)
                # print(self.high_scores_list)
                self.high_score = self.high_scores_list[0]["score"]
        except (FileNotFoundError, ValueError, EOFError, json.JSONDecodeError, AttributeError, IndexError) as e:
            print(e)
            self.high_scores_list = [
              {"name": "---", "score": 0} for _ in range(10)
            ]
            self.high_score = self.high_scores_list[0]["score"]

    def save_scores(self, player_name="---"):
        is_inserted = False
        for i in range(len(self.high_scores_list)):
            if not is_inserted:
                if self.score >= self.high_scores_list[i]["score"]:
                    score_obj = {"name": player_name, "score": self.score}
                    self.high_scores_list.insert(i, score_obj)
                    self.high_scores_list.pop(-1)
                    is_inserted = True
        with open(self.ai_settings.high_score_datafile, 'w') as file:
            json.dump(self.high_scores_list, file)
