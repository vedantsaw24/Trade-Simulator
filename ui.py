import tkinter as tk
from tkinter import ttk, messagebox

class UIManager:
    __slots__ = ("root", "on_start", "left_frame", "right_frame", "exchange_var", "asset_var",
                 "order_type_var", "quantity_var", "volatility_var", "fee_tier_var", "start_button",
                 "output_labels")  # Memory optimization with __slots__

    def __init__(self, root, on_start=None):
        self.root = root
        self.on_start = on_start
        self.root.title("OKX Spot Trade Simulator")
        self.root.geometry("900x400")

        self._configure_grid()
        self._build_input_panel()
        self._build_output_panel()

    def _configure_grid(self):
        self.left_frame = tk.Frame(self.root, padx=10, pady=10)
        self.left_frame.grid(row=0, column=0, sticky='nsew')

        self.right_frame = tk.Frame(self.root, padx=10, pady=10, bg="#f4f4f4")
        self.right_frame.grid(row=0, column=1, sticky='nsew')

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)

    def _build_input_panel(self):
        fields = [
            ("Exchange", ttk.Combobox, {"values": ["OKX"]}),
            ("Spot Asset", ttk.Combobox, {"values": ["BTC-USDT", "ETH-USDT", "SOL-USDT"]}),
            ("Order Type", ttk.Combobox, {"values": ["market"]}),
            ("Quantity (USD)", tk.Entry, {"default": "100"}),
            ("Volatility", tk.Entry, {"default": "0.02"}),
            ("Fee Tier", ttk.Combobox, {"values": ["Tier 1", "Tier 2"]})
        ]

        var_refs = ["exchange_var", "asset_var", "order_type_var", "quantity_var", "volatility_var", "fee_tier_var"]

        for i, ((label, widget_type, options), var_name) in enumerate(zip(fields, var_refs)):
            tk.Label(self.left_frame, text=label).grid(row=i, column=0, sticky='w')

            if widget_type == tk.Entry:
                widget = widget_type(self.left_frame)
                widget.insert(0, options.get("default", ""))
            else:
                widget = widget_type(self.left_frame, values=options["values"])
                widget.current(0)

            widget.grid(row=i, column=1)
            setattr(self, var_name, widget)

        self.start_button = tk.Button(self.left_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=len(fields), column=0, columnspan=2, pady=15)

    def _build_output_panel(self):
        self.output_labels = {}
        fields = [
            "Expected Slippage (USD)", "Expected Fees (USD)", "Market Impact (USD)",
            "Net Cost (USD)", "Maker/Taker (%)", "Internal Latency (ms)"
        ]

        for i, field in enumerate(fields):
            tk.Label(self.right_frame, text=field, anchor='w', bg="#f4f4f4").grid(row=i, column=0, sticky='w', pady=2)
            val = tk.Label(self.right_frame, text="---", bg="#f4f4f4", anchor='w')
            val.grid(row=i, column=1, sticky='w')
            self.output_labels[field] = val

    def start_simulation(self):
        try:
            quantity = float(self.quantity_var.get().strip())
            volatility = float(self.volatility_var.get().strip())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")
            return

        fee_tier = self.fee_tier_var.get()
        if self.on_start:
            self.root.after(0, lambda: self.on_start(quantity, volatility, fee_tier))  # UI-safe callback

    def update_output(self, output_data):
        for key, val in output_data.items():
            label = self.output_labels.get(key)
            if label:
                label.config(text=val)
