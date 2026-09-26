import csv
import os
import tkinter as tk

# ---------- 1. SETUP ----------
FOLDER = os.path.dirname(os.path.abspath(__file__))
TEXTS_FILE = os.path.join(FOLDER, "texts.txt")
LABELS_FILE = os.path.join(FOLDER, "labels.csv")

# ---------- 2. LOAD ----------
with open(TEXTS_FILE, encoding="utf-8") as f:
    texts = [line.strip() for line in f if line.strip()]

done = set()
if os.path.exists(LABELS_FILE):
    with open(LABELS_FILE, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip the header row
        for row in reader:
            done.add(row[0])

remaining = [t for t in texts if t not in done]

# ---------- 3. ACTIONS ----------
def save_label(label):
    if not remaining:
        return
    new_file = not os.path.exists(LABELS_FILE)
    with open(LABELS_FILE, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["text", "label"])
        writer.writerow([remaining[0], label])
    remaining.pop(0)
    show_next()

def show_next():
    counter.config(text=f"{len(texts) - len(remaining)} / {len(texts)} labeled")
    if remaining:
        sentence.config(text=remaining[0])
    else:
        sentence.config(text="All done!")
        for button in buttons:
            button.config(state="disabled")

# ---------- 4. WINDOW ----------
window = tk.Tk()
window.title("Label Tool")
window.geometry("650x300")

counter = tk.Label(window, font=("Arial", 11))
counter.pack(pady=10)

sentence = tk.Label(window, font=("Arial", 16), wraplength=550)
sentence.pack(pady=30)

button_row = tk.Frame(window)
button_row.pack()

creepy_button = tk.Button(button_row, text="Creepy (1)", width=12,
                          command=lambda: save_label("creepy"))
normal_button = tk.Button(button_row, text="Not creepy(2)", width=12,
                          command=lambda: save_label("not creepy"))
skip_button = tk.Button(button_row, text="Skip(3)", width=12,
                        command=lambda: save_label("skip"))

creepy_button.pack(side="left", padx=10)
normal_button.pack(side="left", padx=10)
skip_button.pack(side="left", padx=10)
window.bind("1", lambda event: save_label("creepy"))
window.bind("2", lambda event: save_label ("not creepy"))
window.bind("3", lambda event: save_label ("skip"))
window.bind("z", lambda event: undo())
window.bind("s", lambda event: show_stats())

buttons = [creepy_button, normal_button, skip_button]

show_next()
def undo():
    if not os.path.exists(LABELS_FILE):
        return
    with open(LABELS_FILE, encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    if len(rows) <= 1:  # only the header left, nothing to undo
        return
    last_row = rows.pop()
    with open(LABELS_FILE, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)
    remaining.insert(0, last_row[0])
    for button in buttons:
        button.config(state="normal")
    show_next()
def show_stats():
    counts = {"creepy": 0, "not creepy": 0, "skip": 0}
    if os.path.exists(LABELS_FILE):
        with open(LABELS_FILE, encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the header row
            for row in reader:
                label = row[1]
                if label in counts:
                    counts[label] += 1

    total = sum(counts.values())
    lines = [f"Total labeled: {total}", ""]
    for label, count in counts.items():
        bar = "█" * count
        lines.append(f"{label:<11} {count:>3}  {bar}")

    stats_window = tk.Toplevel(window)
    stats_window.title("Stats")
    tk.Label(stats_window, text="\n".join(lines),
             font=("Consolas", 12), justify="left").pack(padx=20, pady=20)
window.mainloop()