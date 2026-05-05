# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

from noodle_shop import (
    BASE_OPTIONS,
    TOPPING_OPTION_MAP,
    TOPPING_OPTIONS,
    compose_order,
    is_topping_allowed_for_base,
    unwrap_order,
)


RECEIPT_CARD_HEIGHT = 520
DESCRIPTION_CARD_HEIGHT = 150


class NoodleShopApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("遥记天天见面")
        self.root.geometry("1560x900")
        self.root.minsize(1420, 800)
        self.root.configure(bg="#f6efe6")

        self.base_var = tk.StringVar(value=BASE_OPTIONS[0]["key"])
        self.topping_vars: dict[str, tk.IntVar] = {
            option["key"]: tk.IntVar(value=0) for option in TOPPING_OPTIONS
        }
        self.counter_buttons: dict[str, dict[str, tk.Button]] = {}
        self.status_var = tk.StringVar(value="请选择面底和配料。")
        self.total_var = tk.StringVar(value="0.00 元")

        self._configure_style()
        self._build_layout()
        self.refresh_preview()

    def _configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("App.TFrame", background="#f6efe6")
        style.configure("Card.TFrame", background="#fffaf4", relief="flat")
        style.configure("Panel.TLabelframe", background="#fffaf4", borderwidth=0)
        style.configure("Panel.TLabelframe.Label", background="#fffaf4", foreground="#6b3f22", font=("Microsoft YaHei UI", 12, "bold"))
        style.configure("Base.TRadiobutton", background="#fffaf4", foreground="#4d3427", font=("Microsoft YaHei UI", 11))
        style.map("Base.TRadiobutton", background=[("active", "#fffaf4")])
        style.configure("Counter.TLabel", background="#fffaf4", foreground="#6b3f22", font=("Segoe UI", 11, "bold"))
        style.configure("Title.TLabel", background="#f6efe6", foreground="#6b3f22", font=("Microsoft YaHei UI", 24, "bold"))
        style.configure("SectionTitle.TLabel", background="#fffaf4", foreground="#6b3f22", font=("Microsoft YaHei UI", 13, "bold"))
        style.configure("Soft.TButton", font=("Microsoft YaHei UI", 10), padding=(12, 8), background="#ead8c7", foreground="#6b3f22", borderwidth=0)
        style.map("Soft.TButton", background=[("active", "#dec5af")])
        style.configure("Slim.Vertical.TScrollbar", background="#d8b89d", troughcolor="#f4e7da", bordercolor="#f4e7da", arrowcolor="#8b5e3c", lightcolor="#d8b89d", darkcolor="#d8b89d", width=10)
        style.map("Slim.Vertical.TScrollbar", background=[("active", "#c98a56")])

    def _build_layout(self):
        main = ttk.Frame(self.root, style="App.TFrame", padding=18)
        main.pack(fill="both", expand=True)

        header = ttk.Frame(main, style="App.TFrame")
        header.pack(fill="x", pady=(0, 16))
        ttk.Label(header, text="遥记天天见面", style="Title.TLabel").pack(anchor="w")

        body = ttk.Frame(main, style="App.TFrame")
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=5, minsize=360)
        body.columnconfigure(1, weight=5, minsize=420)
        body.columnconfigure(2, weight=6, minsize=500)
        body.rowconfigure(0, weight=1)

        left = ttk.Frame(body, style="Card.TFrame", padding=16)
        center = ttk.Frame(body, style="Card.TFrame", padding=16)
        right = ttk.Frame(body, style="Card.TFrame", padding=16)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        center.grid(row=0, column=1, sticky="nsew", padx=10)
        right.grid(row=0, column=2, sticky="nsew", padx=(10, 0))

        self._build_base_panel(left)
        self._build_topping_panel(center)
        self._build_receipt_panel(right)

        footer = ttk.Frame(main, style="App.TFrame")
        footer.pack(fill="x", pady=(16, 0))
        ttk.Button(footer, text="清空选择", style="Soft.TButton", command=self.reset_order).pack(side="left")

        status = tk.Label(
            main,
            textvariable=self.status_var,
            anchor="w",
            bg="#f0e2d3",
            fg="#7a4d2f",
            font=("Microsoft YaHei UI", 10),
            padx=12,
            pady=10,
        )
        status.pack(fill="x", pady=(12, 0))

    def _build_base_panel(self, parent: ttk.Frame):
        ttk.Label(parent, text="面底", style="SectionTitle.TLabel").pack(anchor="w", pady=(0, 14))

        for option in BASE_OPTIONS:
            card = tk.Frame(parent, bg="#fff3e7", bd=0, highlightthickness=0)
            card.pack(fill="x", pady=6)
            card.columnconfigure(0, weight=1)
            radio = ttk.Radiobutton(
                card,
                text=option["label"],
                variable=self.base_var,
                value=option["key"],
                style="Base.TRadiobutton",
                command=self.refresh_preview,
            )
            radio.grid(row=0, column=0, sticky="w", padx=12, pady=(10, 2))
            tk.Label(
                card,
                text=f"{option['price']:.2f} 元 · {option['group']}",
                bg="#fff3e7",
                fg="#8b5e3c",
                font=("Microsoft YaHei UI", 9),
            ).grid(row=1, column=0, sticky="w", padx=34, pady=(0, 10))

    def _build_topping_panel(self, parent: ttk.Frame):
        ttk.Label(parent, text="配料", style="SectionTitle.TLabel").pack(anchor="w", pady=(0, 14))

        canvas_holder = tk.Frame(parent, bg="#fffaf4")
        canvas_holder.pack(fill="both", expand=True)

        self.topping_canvas = tk.Canvas(
            canvas_holder,
            bg="#fffaf4",
            highlightthickness=0,
            bd=0,
        )
        topping_scrollbar = ttk.Scrollbar(canvas_holder, orient="vertical", style="Slim.Vertical.TScrollbar", command=self.topping_canvas.yview)
        self.topping_canvas.configure(yscrollcommand=topping_scrollbar.set)

        topping_scrollbar.pack(side="right", fill="y")
        self.topping_canvas.pack(side="left", fill="both", expand=True)

        self.topping_content = tk.Frame(self.topping_canvas, bg="#fffaf4")
        self.topping_canvas_window = self.topping_canvas.create_window((0, 0), window=self.topping_content, anchor="nw")
        self.topping_content.bind("<Configure>", lambda event: self._sync_scroll_region(self.topping_canvas))
        self.topping_canvas.bind("<Configure>", lambda event: self.topping_canvas.itemconfigure(self.topping_canvas_window, width=event.width))

        group_order = ["主浇头", "配菜", "加量"]
        for group_name in group_order:
            section = ttk.LabelFrame(self.topping_content, text=group_name, style="Panel.TLabelframe", padding=12)
            section.pack(fill="x", pady=(0, 12))
            options = [option for option in TOPPING_OPTIONS if option["group"] == group_name]
            for option in options:
                self._build_counter_row(section, option)

        self._bind_mousewheel(self.topping_canvas)

    def _build_counter_row(self, parent: ttk.LabelFrame, option: dict):
        row = tk.Frame(parent, bg="#fffaf4")
        row.pack(fill="x", pady=6)

        label_box = tk.Frame(row, bg="#fffaf4")
        label_box.pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Label(
            label_box,
            text=option["label"],
            bg="#fffaf4",
            fg="#4d3427",
            font=("Microsoft YaHei UI", 11, "bold"),
        ).pack(anchor="w")
        tk.Label(
            label_box,
            text=f"单价 {option['price']:.2f} 元",
            bg="#fffaf4",
            fg="#9a6d4b",
            font=("Microsoft YaHei UI", 9),
        ).pack(anchor="w")

        counter = tk.Frame(row, bg="#f4e5d6")
        counter.pack(side="right")
        minus_button = tk.Button(
            counter,
            text="-",
            command=lambda key=option["key"]: self.change_topping_count(key, -1),
            width=3,
            relief="flat",
            bg="#dec2aa",
            fg="#6b3f22",
            activebackground="#d5b295",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            disabledforeground="#9a806e",
        )
        minus_button.pack(side="left")
        ttk.Label(counter, textvariable=self.topping_vars[option["key"]], style="Counter.TLabel", width=4, anchor="center").pack(side="left", padx=4)
        plus_button = tk.Button(
            counter,
            text="+",
            command=lambda key=option["key"]: self.change_topping_count(key, 1),
            width=3,
            relief="flat",
            bg="#c98a56",
            fg="#ffffff",
            activebackground="#b96c38",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            disabledforeground="#f7eee6",
        )
        plus_button.pack(side="left")
        self.counter_buttons[option["key"]] = {
            "minus": minus_button,
            "plus": plus_button,
        }

    def _build_receipt_panel(self, parent: ttk.Frame):
        ttk.Label(parent, text="小票", style="SectionTitle.TLabel").pack(anchor="w", pady=(0, 12))

        summary_card = tk.Frame(parent, bg="#fff3e7", bd=0, height=DESCRIPTION_CARD_HEIGHT)
        summary_card.pack(fill="x", pady=(0, 12))
        summary_card.pack_propagate(False)
        tk.Label(
            summary_card,
            text="完整描述",
            bg="#fff3e7",
            fg="#6b3f22",
            font=("Microsoft YaHei UI", 12, "bold"),
        ).pack(anchor="w", padx=12, pady=(12, 4))

        desc_box = tk.Frame(summary_card, bg="#fff3e7")
        desc_box.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        desc_scrollbar = ttk.Scrollbar(desc_box, orient="vertical", style="Slim.Vertical.TScrollbar")
        self.desc_text = tk.Text(
            desc_box,
            wrap="word",
            bg="#fff3e7",
            fg="#4d3427",
            font=("Microsoft YaHei UI", 11),
            bd=0,
            relief="flat",
            highlightthickness=0,
            yscrollcommand=desc_scrollbar.set,
        )
        desc_scrollbar.configure(command=self.desc_text.yview)
        self.desc_text.pack(side="left", fill="both", expand=True)
        desc_scrollbar.pack(side="right", fill="y")
        self.desc_text.configure(state="disabled")
        self._bind_mousewheel(self.desc_text)

        receipt_card = tk.Frame(parent, bg="#6b3f22", height=RECEIPT_CARD_HEIGHT)
        receipt_card.pack(fill="x", expand=False, pady=(0, 0))
        receipt_card.pack_propagate(False)
        tk.Label(
            receipt_card,
            text="今日小票",
            bg="#6b3f22",
            fg="#fff6eb",
            font=("Microsoft YaHei UI", 16, "bold"),
        ).pack(anchor="w", padx=14, pady=(14, 8))

        receipt_box = tk.Frame(receipt_card, bg="#6b3f22")
        receipt_box.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        receipt_scrollbar = ttk.Scrollbar(receipt_box, orient="vertical", style="Slim.Vertical.TScrollbar")
        self.receipt_text = tk.Text(
            receipt_box,
            font=("Consolas", 12),
            bg="#fffaf4",
            fg="#4d3427",
            bd=0,
            relief="flat",
            padx=14,
            pady=14,
            highlightthickness=0,
            yscrollcommand=receipt_scrollbar.set,
        )
        receipt_scrollbar.configure(command=self.receipt_text.yview)
        self.receipt_text.pack(side="left", fill="both", expand=True)
        receipt_scrollbar.pack(side="right", fill="y")
        self.receipt_text.configure(state="disabled")
        self._bind_mousewheel(self.receipt_text)

        total_row = tk.Frame(parent, bg="#fffaf4")
        total_row.pack(fill="x", pady=(14, 0))
        tk.Label(
            total_row,
            text="合计",
            bg="#fffaf4",
            fg="#8b5e3c",
            font=("Microsoft YaHei UI", 11),
        ).pack(side="left")
        tk.Label(
            total_row,
            textvariable=self.total_var,
            bg="#fffaf4",
            fg="#b14f1d",
            font=("Segoe UI", 24, "bold"),
        ).pack(side="right")

    def _sync_scroll_region(self, canvas: tk.Canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfigure(self.topping_canvas_window, width=canvas.winfo_width())

    def _bind_mousewheel(self, widget: tk.Widget):
        widget.bind("<Enter>", lambda event, target=widget: self._activate_mousewheel(target))
        widget.bind("<Leave>", lambda event: self._deactivate_mousewheel())

    def _activate_mousewheel(self, widget: tk.Widget):
        self.active_scroll_target = widget
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        self.root.bind_all("<Button-4>", self._on_mousewheel)
        self.root.bind_all("<Button-5>", self._on_mousewheel)

    def _deactivate_mousewheel(self):
        self.active_scroll_target = None
        self.root.unbind_all("<MouseWheel>")
        self.root.unbind_all("<Button-4>")
        self.root.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        target = getattr(self, "active_scroll_target", None)
        if target is None:
            return
        if getattr(event, "delta", 0):
            step = -1 if event.delta > 0 else 1
        elif getattr(event, "num", None) == 4:
            step = -1
        else:
            step = 1
        target.yview_scroll(step, "units")

    def _sync_topping_controls(self):
        base_key = self.base_var.get()
        for option in TOPPING_OPTIONS:
            key = option["key"]
            buttons = self.counter_buttons.get(key)
            if buttons is None:
                continue

            count = self.topping_vars[key].get()
            max_count = option["max"]
            incompatible = not is_topping_allowed_for_base(base_key, key)
            minus_disabled = count <= 0
            plus_disabled = incompatible or (max_count is not None and count >= max_count)

            buttons["minus"].configure(
                state=tk.DISABLED if minus_disabled else tk.NORMAL,
                bg="#ead8c7" if minus_disabled else "#dec2aa",
                fg="#9a806e" if minus_disabled else "#6b3f22",
                activebackground="#ead8c7" if minus_disabled else "#d5b295",
                cursor="arrow" if minus_disabled else "hand2",
            )
            buttons["plus"].configure(
                state=tk.DISABLED if plus_disabled else tk.NORMAL,
                bg="#e3c8ad" if plus_disabled else "#c98a56",
                fg="#f7eee6" if plus_disabled else "#ffffff",
                activebackground="#e3c8ad" if plus_disabled else "#b96c38",
                cursor="arrow" if plus_disabled else "hand2",
            )

    def change_topping_count(self, key: str, delta: int):
        option = TOPPING_OPTION_MAP[key]
        if delta > 0 and not is_topping_allowed_for_base(self.base_var.get(), key):
            self.status_var.set(f"当前面底不能搭配{option['label']}。")
            return
        current = self.topping_vars[key].get()
        next_value = max(0, current + delta)
        if option["max"] is not None:
            next_value = min(option["max"], next_value)
        self.topping_vars[key].set(next_value)
        self.refresh_preview()
        if option["max"] is not None and next_value == option["max"] and delta > 0:
            self.status_var.set(f"{option['label']}最多可选 {option['max']} 份。")

    def selected_toppings(self) -> list[str]:
        toppings: list[str] = []
        base_key = self.base_var.get()
        for option in TOPPING_OPTIONS:
            if not is_topping_allowed_for_base(base_key, option["key"]):
                continue
            count = self.topping_vars[option["key"]].get()
            toppings.extend([option["key"]] * count)
        return toppings

    def _normalize_toppings_for_base(self):
        base_key = self.base_var.get()
        for option in TOPPING_OPTIONS:
            if not is_topping_allowed_for_base(base_key, option["key"]):
                self.topping_vars[option["key"]].set(0)

    def refresh_preview(self):
        self._normalize_toppings_for_base()
        noodle = compose_order(self.base_var.get(), self.selected_toppings())
        layers = unwrap_order(noodle)
        total = noodle.cost()

        self._update_description(noodle.get_description())
        self.total_var.set(f"{total:.2f} 元")
        self._update_receipt(layers)
        self._sync_topping_controls()
        self.status_var.set("订单已更新。")

    def _update_description(self, text: str):
        self.desc_text.configure(state="normal")
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert("1.0", text)
        self.desc_text.see(tk.END)
        self.desc_text.yview_moveto(1.0)
        self.desc_text.configure(state="disabled")

    def _update_receipt(self, layers: list[dict]):
        lines = [
            "遥记天天见面",
            "-" * 26,
        ]
        for layer in layers:
            name = layer["label"]
            price = layer["price"]
            lines.append(f"{name:<14} {price:>6.2f} 元")
        lines.extend([
            "-" * 26,
            "欢迎下次光临",
        ])

        self.receipt_text.configure(state="normal")
        self.receipt_text.delete("1.0", tk.END)
        self.receipt_text.insert("1.0", "\n".join(lines))
        self.receipt_text.see(tk.END)
        self.receipt_text.yview_moveto(1.0)
        self.receipt_text.configure(state="disabled")

    def reset_order(self):
        self.base_var.set(BASE_OPTIONS[0]["key"])
        for variable in self.topping_vars.values():
            variable.set(0)
        self.refresh_preview()
        self.status_var.set("已清空配料并恢复默认面底。")


def main():
    root = tk.Tk()
    NoodleShopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
