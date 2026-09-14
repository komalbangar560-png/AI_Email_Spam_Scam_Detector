import re


def check_scam_risk(email):
    email_lower = email.lower()

    risk_score = 0
    reasons = []

    scam_keywords = [
        "otp",
        "password",
        "bank account",
        "credit card",
        "debit card",
        "verify your account",
        "click here",
        "urgent",
        "immediately",
        "prize",
        "lottery",
        "winner",
        "claim your reward",
        "send money",
        "transfer money",
        "refund",
        "investment",
        "crypto",
        "bitcoin",
        "login",
        "account suspended"
    ]

    for keyword in scam_keywords:
        if keyword in email_lower:
            risk_score += 10
            reasons.append("Contains suspicious term: " + keyword)

    urls = re.findall(r"https?://\S+|www\.\S+", email_lower)

    if urls:
        risk_score += 20
        reasons.append("Contains a link")

    if "urgent" in email_lower or "immediately" in email_lower:
        risk_score += 15
        reasons.append("Uses urgent language")

    if risk_score >= 50:
        risk = "High"
    elif risk_score >= 25:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "risk": risk,
        "score": min(risk_score, 100),
        "reasons": reasons
    }