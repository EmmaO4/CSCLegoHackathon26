import random

def recommended_hours(units: int, difficulty: str, target: str) -> int:
    base = 2.5 * units  # baseline hrs/week
    diff_mult = {"Easy": 0.85, "Normal": 1.0, "Hard": 1.2}.get(difficulty, 1.0)
    target_mult = {"Pass": 0.9, "B": 1.0, "A": 1.15}.get(target, 1.0)
    hrs = base * diff_mult * target_mult
    return max(1, int(round(hrs)))

QUOTES = [
    "Small steps every day beat last-minute panic.",
    "Consistency is a superpower.",
    "Your future self is watching—make them proud.",
    "Study like you respect your goals.",
    "Progress over perfection."
]

def burnout_assessment(weekly_hours: int, today_minutes: int, avg_mood: float) -> tuple[str, str]:
    # simple rule-based scoring (hackathon-friendly)
    score = 0
    if weekly_hours >= 35: score += 2
    elif weekly_hours >= 25: score += 1
    if today_minutes < 30: score += 1
    if avg_mood <= 2.2: score += 2
    elif avg_mood <= 3.0: score += 1

    if score >= 4:
        return ("High", "Reduce pressure: pick 1 priority class today + take a real break.")
    if score >= 2:
        return ("Medium", "You’re okay, but don’t grind. Use short focused sessions + breaks.")
    return ("Low", "Good pace. Keep a steady routine and protect your sleep.")

def wellness_pack(level: str):
    if level == "High":
        acts = ["10-min walk outside", "Stretch + water (5 min)", "Clean desk reset (3 min)", "Text a friend", "Plan tomorrow in 3 bullets"]
    elif level == "Medium":
        acts = ["Pomodoro 25/5", "2-min breathing", "Quick snack + water", "Change study location", "Do easiest task first"]
    else:
        acts = ["Keep streak alive (15 min)", "Review flashcards", "Prep tomorrow’s task list", "Reward yourself after session"]
    return acts, random.choice(QUOTES)
