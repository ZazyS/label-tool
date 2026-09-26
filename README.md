# Label Tool

A simple data labeling app built with Python and tkinter.
It shows sentences one at a time, you label each one with a click,
and every answer is saved to a CSV file, the same format real AI training data uses.

## Features

- Keyboard shortcuts: 1 = Creepy, 2 = not creepy, 3 = skip
- Undo the last label with Z
- One sentence at a time, three buttons: Creepy / Not creepy / Skip
- Every label is saved instantly to `labels.csv`
- Progress counter
- Resume: close it halfway, and it continues where you stopped
- Stats window with S: label counts with bars, to check if the dataset is balanced
- Custom categories: edit categories.txt (one per line, up to 8). Skip is added automatically

## How to run

1. Put your categories in categories.txt, one per line.
2. Put the sentences you want to label in `texts.txt`, one per line
3. Run `python labeler.py`
4. Results appear in `labels.csv`

No installs needed, only Python's built-in libraries.

## Labeling guideline

- **Creepy:** something impossible or unexplained happens
- **Not creepy:** there's a normal explanation, even if the situation is strange
- **Kinda creepy:** unsettling, but a normal explanation is possible, it's just not stated.
  (e.g. "The wind rattled the windows all night." The cause is stated, so not creepy)

A consistent rule matters more than gut feeling: two annotators labeling
by vibe will disagree, two annotators following the same guideline won't.

## Example output

`labels.csv` contains 30 sentences I labeled with this tool.

## Agreement check

`compare.py` compares two annotators' labels on the same sentences
and lists where they disagree (inter-annotator agreement).

1. Rename your `labels.csv` to `labels_me.csv`
2. A second annotator labels the same sentences, then rename their `labels.csv` to `labels_other.csv`
3. Run `python compare.py`

My test: labeling once by the guideline and once by gut feeling gave 93% agreement.
The two disagreements were exactly the borderline cases (weather and smells),
which shows where the guideline needs a clearer rule.