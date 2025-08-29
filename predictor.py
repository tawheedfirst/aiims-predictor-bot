# predictor.py
import math
from scipy.stats import norm

# === Model parameters (do not change, derived earlier) ===
K_MEAN = 1.041
K_CI_LO = 1.006
K_CI_HI = 1.075
K_SD   = (K_CI_HI - K_CI_LO) / (2.0 * 1.96)

def predict_aiims(gmc_input, user_score, gmc_unc=10.0, buffer=5, conf=97.5):
    gmc_sd = gmc_unc / 1.96
    mu = K_MEAN * gmc_input
    var = (gmc_input**2) * (K_SD**2) + (K_MEAN**2) * (gmc_sd**2)
    sd = math.sqrt(max(var, 1e-9))

    # Probability
    z = (user_score - mu) / sd
    prob = norm.cdf(z)

    # Safe target
    zt = norm.ppf(conf / 100.0)
    safe = mu + zt * sd + buffer

    return {
        "gmc_input": gmc_input,
        "user_score": user_score,
        "predicted_mean": round(mu, 2),
        "predicted_sd": round(sd, 2),
        "probability_pct": round(prob * 100, 2),
        "recommended_safe_target": round(safe, 2),
        "advice": give_advice(prob)
    }

def give_advice(prob):
    if prob >= 0.84:
        return "✅ Very strong chance. Keep steady with PW mocks and revision."
    if prob >= 0.50:
        return "🟢 Good chance. Push +5–15 marks in upcoming PW tests."
    if prob >= 0.10:
        return "🟠 Moderate chance. Work for +15–40 marks improvement in PW boosters."
    return "🔴 Low chance. Focus on fundamentals and aim >40 marks jump."
