import csv
import os

FOLDER = os.path.dirname(os.path.abspath(__file__))
FILE_ME = os.path.join(FOLDER, "labels_me.csv")
FILE_OTHER = os.path.join(FOLDER, "labels_other.csv")

def load_labels(path):
    labels = {}
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip the header row
        for row in reader:
            labels[row[0]] = row[1]
    return labels

me = load_labels(FILE_ME)
other = load_labels(FILE_OTHER)

shared = [text for text in me if text in other]
agreed = [text for text in shared if me[text] == other[text]]
disagreed = [text for text in shared if me[text] != other[text]]

if not shared:
    print("No sentences in common, nothing to compare.")
else:
    percent = len(agreed) / len(shared) * 100
    print(f"Agreement: {len(agreed)} / {len(shared)} ({percent:.0f}%)")
    print()
    if disagreed:
        print("Disagreements:")
        for text in disagreed:
            print(f'- "{text}"')
            print(f"    me: {me[text]}  |  other: {other[text]}")
    else:
        print("No disagreements. Perfect match!")