import tkinter as tk
import time
import csv
from datetime import datetime
from queue import Queue
from threading import Thread, Lock
import atexit

from ui import UIManager
from ws_client.websocket_handler import WebSocketClient
from processor.tick_processor import TickProcessor

LATENCY_LOG_FILE = "latency_log.csv"
LOG_FLUSH_INTERVAL = 1  # in seconds

class LatencyLogger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.queue = Queue()
        self.lock = Lock()
        self.running = True
        self._setup_csv()
        self._start_flusher()
        atexit.register(self.stop)

    def _setup_csv(self):
        with open(self.log_file, mode='w', newline='') as file:
            csv.writer(file).writerow(["Timestamp", "ProcessingLatency(ms)", "UILatency(ms)", "TotalLatency(ms)"])

    def log(self, timestamp, processing, ui, total):
        self.queue.put((timestamp, processing, ui, total))

    def _start_flusher(self):
        def flush():
            while self.running:
                time.sleep(LOG_FLUSH_INTERVAL)
                self._flush_queue()

        Thread(target=flush, daemon=True).start()

    def _flush_queue(self):
        with self.lock, open(self.log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            while not self.queue.empty():
                writer.writerow(self.queue.get())

    def stop(self):
        self.running = False
        self._flush_queue()

class MainApp:
    def __init__(self, root):
        self.processor = None
        self.client = None
        self.logger = LatencyLogger(LATENCY_LOG_FILE)
        self.ui = UIManager(root, on_start=self.start_simulation)

    def start_simulation(self, quantity, volatility, fee_tier):
        self.processor = TickProcessor(quantity, volatility, fee_tier)
        asset = self.ui.asset_var.get() + "-SWAP"

        if self.client:
            self.client.close()

        self.client = WebSocketClient(symbol=asset, on_tick=self.on_tick)
        self.client.connect()

    def on_tick(self, tick_data):
        if not self.processor:
            return

        t0 = time.perf_counter()
        output = self.processor.process_tick(tick_data)
        t1 = time.perf_counter()

        self.ui.update_output(output)
        t2 = time.perf_counter()

        processing_latency = (t1 - t0) * 1000
        ui_latency = (t2 - t1) * 1000
        total_latency = (t2 - t0) * 1000

        print(f"[Latency] Processing: {processing_latency:.2f} ms | UI: {ui_latency:.2f} ms | Total: {total_latency:.2f} ms")

        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.logger.log(now, round(processing_latency, 2), round(ui_latency, 2), round(total_latency, 2))

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
