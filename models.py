import math

# 1. Almgren–Chriss Market Impact Model
def calculate_market_impact(
    quantity,
    volatility,
    daily_volume=1_000_000,
    eta=0.142,      # temporary impact coefficient
    gamma=2.5e-6,   # permanent impact coefficient
    lambda_risk=1e-6,  # risk aversion (for advanced users)
    time_horizon=1     # trading time in days
):
    q = float(quantity)
    V = float(daily_volume)

    temp_impact = eta * (q / V) * math.sqrt(time_horizon)
    perm_impact = gamma * q
    impact_cost = temp_impact + perm_impact

    return round(impact_cost, 5)


# 2. Regression-Based Slippage Estimation (Linear Regression with interaction term)
def predict_slippage(quantity, volatility):
    q = float(quantity)
    sigma = float(volatility)

    # Coefficients (mocked for now — can be trained)
    beta_0 = 0.005
    beta_1 = 0.0003
    beta_2 = 0.7
    beta_3 = 0.00001  # interaction term (q * sigma)

    slippage = beta_0 + beta_1 * q + beta_2 * sigma + beta_3 * q * sigma
    return round(slippage, 5)


# 3. Logistic Model for Maker/Taker Prediction
def predict_maker_taker_ratio(volatility, sensitivity=50, threshold=0.08):
    """
    Returns: (maker_probability, taker_probability)
    - sensitivity: how steeply the logistic curve transitions
    - threshold: volatility at which probability is 50%
    """
    sigma = float(volatility)
    z = -sensitivity * (sigma - threshold)

    maker_prob = 1 / (1 + math.exp(-z))
    taker_prob = 1 - maker_prob
    return round(maker_prob, 4), round(taker_prob, 4)
