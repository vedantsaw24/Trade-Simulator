import websocket
import json
import threading

class WebSocketClient:
    def __init__(self, symbol="BTC-USDT-SWAP", on_tick=None):
        self.url = f"wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/{symbol}"
        self.ws = None
        self.on_tick = on_tick

    def connect(self):
        def on_message(ws, message):
            try:
                data = json.loads(message)
                if "asks" in data and "bids" in data:
                    if self.on_tick:
                        self.on_tick(data)
            except Exception as e:
                print("[WebSocket Error]", e)

        self.ws = websocket.WebSocketApp(self.url, on_message=on_message)
        thread = threading.Thread(target=self.ws.run_forever)
        thread.daemon = True
        thread.start()

    def close(self):
        if self.ws:
            self.ws.close()
