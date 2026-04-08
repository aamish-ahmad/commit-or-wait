from .environment import RubiconEnvironment

def grade_task(task: str, actions: list) -> float:
    env = RubiconEnvironment(task=task)
    env.reset()
    total_reward = 0.0
    done = False
    for action in actions:
        if done:
            break
        obs, reward, done, info = env.step(action)
        total_reward += reward.value
    score = min(1.0, max(0.0, (total_reward + 1.0) / 2.0))
    return round(score, 2)

def grade_easy() -> float:
    actions = ["inspect_headers", "inspect_headers", "escalate_phishing"]
    return grade_task("easy", actions)

def grade_medium() -> float:
    actions = ["inspect_headers", "analyze_process", "check_network", "escalate_malware"]
    return grade_task("medium", actions)

def grade_hard() -> float:
    actions = ["inspect_headers", "inspect_headers", "analyze_process", "check_network", "escalate_malware"]
    return grade_task("hard", actions)

if __name__ == "__main__":
    print(f"easy:   {grade_easy()}")
    print(f"medium: {grade_medium()}")
    print(f"hard:   {grade_hard()}")
