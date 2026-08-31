import json
import os
from game.config import ACHIEVEMENTS

SAVE_FILE = 'scores.json'

class HighScoreManager:
    def __init__(self):
        self.high_score_classic = 0
        self.high_score_overdrive = 0
        self.total_distance = 0
        self.total_coins = 0
        self.total_destructions = 0
        self.runs_played = 0
        self.unlocked_achievements = []
        self.load()

    def get_high_score(self, mode_index=0):
        if mode_index == 1:
            return self.high_score_overdrive
        return self.high_score_classic

    @property
    def high_score(self):
        return max(self.high_score_classic, self.high_score_overdrive)

    def load(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.high_score_classic = data.get('high_score_classic', data.get('high_score', 0))
                    self.high_score_overdrive = data.get('high_score_overdrive', 0)
                    self.total_distance = data.get('total_distance', 0)
                    self.total_coins = data.get('total_coins', 0)
                    self.total_destructions = data.get('total_destructions', 0)
                    self.runs_played = data.get('runs_played', 0)
                    self.unlocked_achievements = data.get('unlocked_achievements', [])
            except Exception:
                pass

    def save(self):
        try:
            data = {
                'high_score_classic': self.high_score_classic,
                'high_score_overdrive': self.high_score_overdrive,
                'high_score': self.high_score,
                'total_distance': self.total_distance,
                'total_coins': self.total_coins,
                'total_destructions': self.total_destructions,
                'runs_played': self.runs_played,
                'unlocked_achievements': self.unlocked_achievements
            }
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def unlock_achievement(self, ach_id):
        if ach_id not in self.unlocked_achievements:
            self.unlocked_achievements.append(ach_id)
            self.save()
            for ach in ACHIEVEMENTS:
                if ach['id'] == ach_id:
                    return ach
        return None

    def record_run(self, score, distance, coins, destructions=0, mode_index=0):
        self.runs_played += 1
        self.total_distance += int(distance)
        self.total_coins += int(coins)
        self.total_destructions += int(destructions)
        is_new_high = False

        if mode_index == 1:
            if score > self.high_score_overdrive:
                self.high_score_overdrive = int(score)
                is_new_high = True
        else:
            if score > self.high_score_classic:
                self.high_score_classic = int(score)
                is_new_high = True

        self.save()
        return is_new_high
