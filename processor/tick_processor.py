import time
from models import calculate_market_impact, predict_slippage, predict_maker_taker_ratio

class TickProcessor:
    def __init__(self, quantity, volatility, fee_tier):
        self.quantity = quantity
        self.volatility = volatility
        self.fee_tier = fee_tier
        self.maker_fee, self.taker_fee = self.get_fees()

    def get_fees(self):
        return (0.0010, 0.0015) if self.fee_tier == "Tier 1" else (0.0008, 0.0012)

    def process_tick(self, tick):
        start_time = time.time()  # Start latency timer

        if not tick or "bids" not in tick or "asks" not in tick:
            print("[TickProcessor Warning] Invalid tick data received.")
            return {
                "Expected Slippage (USD)": "---",
                "Expected Fees (USD)": "---",
                "Market Impact (USD)": "---",
                "Net Cost (USD)": "---",
                "Maker/Taker (%)": "---",
                "Internal Latency (ms)": "---"
            }

        best_bid = float(tick["bids"][0][0])
        best_ask = float(tick["asks"][0][0])
        mid_price = (best_bid + best_ask) / 2

        slippage = predict_slippage(self.quantity, self.volatility)
        market_impact = calculate_market_impact(self.quantity, self.volatility)
        maker_prob, taker_prob = predict_maker_taker_ratio(self.volatility)

        fees = self.quantity * mid_price * (maker_prob * self.maker_fee + taker_prob * self.taker_fee)
        net_cost = slippage + market_impact + fees

        latency_ms = (time.time() - start_time) * 1000  # End latency timer

        return {
            "Expected Slippage (USD)": f"{slippage:.4f}",
            "Expected Fees (USD)": f"{fees:.4f}",
            "Market Impact (USD)": f"{market_impact:.4f}",
            "Net Cost (USD)": f"{net_cost:.4f}",
            "Maker/Taker (%)": f"{maker_prob*100:.1f}/{taker_prob*100:.1f}",
            "Internal Latency (ms)": f"{latency_ms:.2f}"
        }
