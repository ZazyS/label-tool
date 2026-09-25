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

creepy_button = tk.Button(button_row, text="Creepy", width=12,
                          command=lambda: save_label("creepy"))
normal_button = tk.Button(button_row, text="Not creepy", width=12,
                          command=lambda: save_label("not creepy"))
skip_button = tk.Button(button_row, text="Skip", width=12,
                        command=lambda: save_label("skip"))

creepy_button.pack(side="left", padx=10)
normal_button.pack(side="left", padx=10)
skip_button.pack(side="left", padx=10)

buttons = [creepy_button, normal_button, skip_button]

show_next()
window.mainloop()