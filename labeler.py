import csv
import os
import tkinter as tk

# ---------- 1. SETUP ----------
FOLDER = os.path.dirname(os.path.abspath(__file__))
TEXTS_FILE = os.path.join(FOLDER, "texts.txt")
LABELS_FILE = os.path.join(FOLDER, "labels.csv")
CATEGORIES_FILE = os.path.join(FOLDER, "categories.txt")

# ---------- 2. LOAD ----------
with open(CATEGORIES_FILE, encoding="utf-8") as f:
    categories = [line.strip() for line in f if line.strip()]
categories = categories[:8]  # max 8, so everything fits on keys 1-9

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
    counts = {}
    for category in categories:
        counts[category] = 0
    counts["skip"] = 0

    if os.path.exists(LABELS_FILE):
        with open(LABELS_FILE, encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
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

# ---------- 4. WINDOW ----------
window = tk.Tk()
window.title("Label Tool")
window.geometry("700x300")

counter = tk.Label(window, font=("Arial", 11))
counter.pack(pady=10)

sentence = tk.Label(window, font=("Arial", 16), wraplength=600)
sentence.pack(pady=30)

button_row = tk.Frame(window)
button_row.pack()

buttons = []
choices = categories + ["skip"]
for number, choice in enumerate(choices, start=1):
    button = tk.Button(button_row, text=f"{choice.capitalize()} ({number})",
                       command=lambda c=choice: save_label(c))
    button.pack(side="left", padx=10)
    buttons.append(button)
    window.bind(str(number), lambda event, c=choice: save_label(c))

window.bind("z", lambda event: undo())
window.bind("s", lambda event: show_stats())

show_next()
window.mainloop()