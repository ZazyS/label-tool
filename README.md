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

## How to run

1. Put the sentences you want to label in `texts.txt`, one per line
2. Run `python labeler.py`
3. Results appear in `labels.csv`

No installs needed, only Python's built-in libraries.

## Labeling guideline

- **Creepy:** something impossible or unexplained happens
- **Not creepy:** there's a normal explanation, even if the situation is strange
  (e.g. "The wind rattled the windows all night." The cause is stated, so not creepy)

A consistent rule matters more than gut feeling: two annotators labeling
by vibe will disagree, two annotators following the same guideline won't.

## Example output

`labels.csv` contains 30 sentences I labeled with this tool.