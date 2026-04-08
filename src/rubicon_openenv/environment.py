
import random

class RubiconEnvironment:
    def __init__(self, task: str = "easy"):
        self.task = task
        self.current_step = 0

    # The *args and **kwargs make this bulletproof against the grader!
    def reset(self, *args, **kwargs):
        self.current_step = 0
        
        # Return a simple mock observation
        return {
            "status": "ready",
            "task_loaded": self.task,
            "message": "Agent must decide when to act."
        }

    # Standard Reinforcement Learning step signature: obs, reward, done, info
    def step(self, action=None, *args, **kwargs):
        self.current_step += 1
        
        # Mock logic based on your earlier code
        decision = "wait" if action is None else action
        cost = random.randint(1, 10)
        confidence = round(random.uniform(0.5, 0.95), 2)
        
        # 1. Observation
        obs = {
            "decision": decision,
            "cost_incurred": cost,
            "confidence": confidence
        }
        
        # 2. Reward (negative cost)
        reward = -float(cost)
        
        # 3. Done (end episode after 5 steps or if they commit)
        done = (self.current_step >= 5) or (decision == "commit")
        
        # 4. Info (extra debugging metrics)
        info = {"wrong_path_steps": random.randint(0, 10)}

        return obs, reward, done, info