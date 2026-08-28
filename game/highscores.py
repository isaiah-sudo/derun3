import json
import os

SAVE_FILE = 'scores.json'

class HighScoreManager:
    def __init__(self):
        self.high_score = 0
        self.total_distance = 0
        self.total_coins = 0
        self.runs_played = 0
        self.load()

    def load(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.high_score = data.get('high_score', 0)
                    self.total_distance = data.get('total_distance', 0)
                    self.total_coins = data.get('total_coins', 0)
                    self.runs_played = data.get('runs_played', 0)
            except Exception:
                pass

    def save(self):
        try:
            data = {
                'high_score': self.high_score,
                'total_distance': self.total_distance,
                'total_coins': self.total_coins,
                'runs_played': self.runs_played
            }
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def record_run(self, score, distance, coins):
        self.runs_played += 1
        self.total_distance += int(distance)
        self.total_coins += int(coins)
        is_new_high = False
        if score > self.high_score:
            self.high_score = int(score)
            is_new_high = True
        self.save()
        return is_new_high
