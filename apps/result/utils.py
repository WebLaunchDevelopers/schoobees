def score_grade(score):
    if score > 90:
        return "A+"
    elif score >= 75 and score <= 90:
        return "A"
    elif score >= 65 and score < 75:
        return "B"
    elif score >= 55 and score < 65:
        return "C"
    elif score >= 45 and score < 55:
        return "D"
    elif score >= 35 and score < 45:
        return "E"
    elif score < 35:
        return "F"