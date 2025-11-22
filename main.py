import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random, time
import sorting as sorts
import searching as searches
import matplotlib.pyplot as plt

# ==== Algorithm Maps ====
SORT_GEN = {
    "Bubble Sort": sorts.bubble_sort_gen,
    "Insertion Sort": sorts.insertion_sort_gen,
    "Selection Sort": sorts.selection_sort_gen,
    "Merge Sort": sorts.merge_sort_gen,
    "Quick Sort": sorts.quick_sort_gen,
    "Tim Sort": sorts.tim_sort_gen
}
SEARCH_GEN = {
    "Linear Search": searches.linear_search_gen,
    "Binary Search": searches.binary_search_gen,
    "Jump Search": searches.jump_search_gen
}

THEME = {
    "bg": "#d183a9",          # lavender background
    "frame": "#71557a",       # golden frame
    "accent": "#f3c8dd",      # purple accent
    "text": "#3a345b",        # dark plum text
    "compare": "#3a345b",     # bright yellow
    "swap": "#4b1535",        # deep violet
    "found": "#71557a",       # mint green
    "done": "#4b1535",         # lantern gold for completion
    "overwrite": "#d183a9"         # lantern gold for completion
}


# ==== Main Application ====
class AlgoVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Algorithm and Time Analysis Visualizer")
        self.geometry("950x700")
        self.configure(bg=THEME["bg"])

        self.mode_var = tk.StringVar(value="Sorting")
        self.algo_var = tk.StringVar()
        self.speed = tk.DoubleVar(value=200)
        self.data = []

        self.create_widgets()
        self.update_algo_list()

    def create_widgets(self):
        title = tk.Label(self, text="✨ Algorithm and Time Analysis Visualizer ✨",
                         font=("Segoe UI", 18, "bold"),
                         bg=THEME["bg"], fg=THEME["text"])
        title.pack(pady=15)

        control = tk.Frame(self, bg=THEME["frame"], bd=3, relief="ridge")
        control.pack(fill="x", padx=10, pady=10)

        tk.Label(control, text="Mode:", bg=THEME["frame"], fg=THEME["text"]).pack(side="left", padx=5)
        ttk.Combobox(control, textvariable=self.mode_var, values=["Sorting", "Searching"],
                     width=12).pack(side="left")
        tk.Label(control, text="Algorithm:", bg=THEME["frame"], fg=THEME["text"]).pack(side="left", padx=5)
        self.algo_combo = ttk.Combobox(control, textvariable=self.algo_var, width=18, state="readonly")
        self.algo_combo.pack(side="left")

        tk.Label(control, text="Speed:", bg=THEME["frame"], fg=THEME["text"]).pack(side="left", padx=5)
        tk.Scale(control, from_=50, to=800, orient="horizontal", variable=self.speed,
                 bg=THEME["frame"], troughcolor=THEME["accent"], length=150).pack(side="left", padx=5)

        ttk.Button(control, text="Generate Data", command=self.generate_data).pack(side="left", padx=6)
        ttk.Button(control, text="Run", command=self.run_algorithm).pack(side="left", padx=6)
        ttk.Button(control, text="Show Time Graph", command=self.show_time_graph).pack(side="right", padx=6)

        self.canvas = tk.Canvas(self, width=880, height=460, bg="white", highlightthickness=3,
                                highlightbackground=THEME["accent"])
        self.canvas.pack(pady=15)

        self.status = tk.Label(self, text="Ready 🌸", bg=THEME["bg"], fg=THEME["text"],
                               font=("Segoe UI", 12))
        self.status.pack(pady=5)

        self.mode_var.trace_add("write", lambda *_: self.update_algo_list())

    def update_algo_list(self):
        if self.mode_var.get() == "Sorting":
            self.algo_combo["values"] = list(SORT_GEN.keys())
            self.algo_combo.current(0)
        else:
            self.algo_combo["values"] = list(SEARCH_GEN.keys())
            self.algo_combo.current(0)

    def generate_data(self):
        val = simpledialog.askstring("Array Size", "Enter number of elements (e.g., 30):")
        if val is None:  # user cancelled
            return
        try:
            n = int(val)
            if n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
            return


        if self.mode_var.get() == "Sorting":
            self.data = [random.randint(10, 200) for _ in range(n)]
        else:
            self.data = sorted([random.randint(10, 200) for _ in range(n)])

        self.draw_data(self.data)
        self.status.config(text=f"Generated array of size {n}")

    def draw_data(self, data, color_map=None):
        self.canvas.delete("all")
        c_width, c_height = 880, 460
        bar_width = c_width / (len(data) + 1)
        offset = 20
        max_height = max(data) if data else 1

        for i, val in enumerate(data):
            x0 = i * bar_width + offset
            y0 = c_height - (val / max_height) * (c_height - 50)
            x1 = (i + 1) * bar_width + offset
            y1 = c_height

            color = color_map.get(i, THEME["accent"]) if color_map else THEME["accent"]
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=THEME["bg"])
            self.canvas.create_text(x0 + 10, y0 - 10, text=str(val), font=("Segoe UI", 8), fill=THEME["text"])
        self.update_idletasks()

    def run_algorithm(self):
        if not self.data:
            messagebox.showwarning("No Data", "Please generate data first!")
            return

        algo_name = self.algo_var.get()
        mode = self.mode_var.get()

        if mode == "Sorting":
            gen = SORT_GEN[algo_name](self.data)
            self.animate(gen)
        else:
            try:
                val = simpledialog.askstring("Search Key", "Enter value to find:")
                if val is None:
                    return  # user cancelled
                target = int(val)
            except ValueError:
                messagebox.showerror("Error", "Invalid key.")
                return

            gen = SEARCH_GEN[algo_name](self.data, target)
            self.animate(gen, search=True, target=target)

    def animate(self, gen, search=False, target=None):
        try:
            action = next(gen)
            color_map = {}

            if search:
                # --- Searching algorithms ---
                if action[0] == "compare":
                    # handle ('compare', index, None, comparisons)
                    index = action[1]
                    comparisons = action[3] if len(action) > 3 else 0
                    color_map[index] = THEME["compare"]
                    self.status.config(
                        text=f"Comparing index {index} (Comparisons: {comparisons})"
                    )

                elif action[0] == "found":
                    # handle ('found', index, comparisons)
                    index = action[1]
                    comparisons = action[2] if len(action) > 2 else 0
                    color_map[index] = THEME["found"]
                    self.status.config(
                        text=f"Found {target} at index {index} (Comparisons: {comparisons})"
                    )
                    self.draw_data(self.data, color_map)
                    return  # stop animation when found

                elif action[0] == "done":
                    # handle ('done', comparisons)
                    comparisons = action[1] if len(action) > 1 else 0
                    if "Found" not in self.status.cget("text"):
                        self.status.config(
                            text=f"{target} not found (Comparisons: {comparisons})"
                        )

            else:
                # --- Sorting algorithms ---
                if action[0] == "compare":
                    i, j = action[1], action[2]
                    color_map[i] = color_map[j] = THEME["compare"]

                elif action[0] == "swap":
                    i, j = action[1], action[2]
                    color_map[i] = color_map[j] = THEME["swap"]

                elif action[0] == "overwrite":
                    i, val = action[1], action[2]
                    color_map[i] = THEME["overwrite"]

                elif action[0] == "done":
                    color_map = {i: THEME["done"] for i in range(len(self.data))}
                    comparisons = action[1] if len(action) > 1 else 0
                    self.status.config(
                        text=f"Sorting completed! 🌟 (Comparisons: {comparisons})"
                    )

            # Draw and schedule next animation frame
            self.draw_data(self.data, color_map)
            self.after(int(self.speed.get()), lambda: self.animate(gen, search, target))

        except StopIteration:
            # Final draw when generator ends
            self.draw_data(self.data, {i: THEME["done"] for i in range(len(self.data))})

    def show_time_graph(self):
        algo = self.algo_var.get()
        mode = self.mode_var.get()
        sizes = [10, 50, 100, 200, 400]
        times = []

        for n in sizes:
            arr = [random.randint(1, 1000) for _ in range(n)]
            start = time.time()
            if mode == "Sorting":
                getattr(sorts, algo.lower().replace(" ", "_"))(arr.copy())
            else:
                arr.sort()
                getattr(searches, algo.lower().replace(" ", "_"))(arr, arr[len(arr)//2])
            times.append(time.time() - start)

        plt.plot(sizes, times, color=THEME["swap"], marker="o")
        plt.title(f"{algo} - Time Complexity", color=THEME["text"])
        plt.xlabel("Input Size (n)")
        plt.ylabel("Time (s)")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.show()


if __name__ == "__main__":
    app = AlgoVisualizer()
    app.mainloop()
