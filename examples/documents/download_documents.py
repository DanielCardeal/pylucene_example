"""Download a list of public domain books using the Guenberg Project library."""
import os

from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers

CWD = os.getcwd()

GUTENBERG_BOOKS = [
    ("MobyDick", 2701),
    ("PrideAndPrejudice", 1342),
    ("Frankenstein", 84),
    ("WarAndPeace", 2600),
    ("LittleWoman", 37106),
    ("Beowulf", 16328),
    ("TheGreatGatsby", 64317),
]

for (title, id) in GUTENBERG_BOOKS:
    print(f"Downloading {title}...", end=" ")
    text = strip_headers(load_etext(id)).strip()
    filepath = f"{title}.txt"
    with open(os.path.join(CWD, filepath), "w") as f:
        f.write(text)
    print("[DONE]")
