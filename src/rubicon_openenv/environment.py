import random
import math
from .models import Observation, Reward, State

TASKS = {
    "easy": {
        "ground_truth": "phishing_attack",
        "signals": ["suspicious_email", "phishing_link", "spoofed_sender"]
    },
    "medium": {
        "ground_truth": "malware_execution",
        "signals": ["process_anomaly", "network_spike", "file_encryption"]
    },
    "hard": {
        "ground_truth": "malware_execution",
        "signals": ["phishing_link", "process_anomaly", "file_encryption"]
    }
}

VALID_ACTIONS = [
    "inspect_headers", "analyze_process", "check_network",
    "review_user_behavior", "escalate_phishing",
    "escalate_malware", "close_false_positive"
]

COMMIT_ACTIONS = {
    "escalate_phishing": "phishing_attack",
    "escalate_malware": "malware_execution",
    "close_false_positive": "false_positive"
}


class RubiconEnvironment:

    def __init__(self, task="easy"):
        self.task = task
        self.max_steps = 10
        self.reset()

    def reset(self):
        self.step_count = 0
        self.action_history = []
        self.done = False

        self.ground_truth = TASKS[self.task]["ground_truth"]
        self.signals = TASKS[self.task]["signals"]

        self.belief = {
            "phishing_attack": 0.33,
            "malware_execution": 0.33,
            "false_positive": 0.34
        }

        return self._get_obs()

    def _entropy(self):
        return -sum(p * math.log(p + 1e-9) for p in self.belief.values())

    def _get_obs(self):
        return Observation(
            step=self.step_count,
            alerts=self.signals[:self.step_count + 1],
            belief=self.belief,
            uncertainty=self._entropy(),
            action_history=self.action_history,
            time_remaining=self.max_steps - self.step_count
        )

    def step(self, action: str):
        self.action_history.append(action)
        self.step_count += 1

        reward_val = 0.1

        if action in COMMIT_ACTIONS:
            chosen = COMMIT_ACTIONS[action]
            if chosen == self.ground_truth:
                return self._get_obs(), Reward(value=1.0, reason="correct"), True, {}
            else:
                return self._get_obs(), Reward(value=0.0, reason="wrong"), True, {}

        done = self.step_count >= self.max_steps

        return self._get_obs(), Reward(value=reward_val, reason="step"), done, {}

    def state(self):
            return State(
            step=self.step_count,
            ground_truth=self.ground_truth,
            belief=self.belief,
            committed=False
        )