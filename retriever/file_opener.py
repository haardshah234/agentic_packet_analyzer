import tkinter as tk
from tkinter import filedialog

def fetch_irs():
    root = tk.Tk()
    root.withdraw()
    filepath = None
    while not filepath:
        filepath = filedialog.askopenfilename(title="Select an IRS", filetypes=[("Word Documents","*.doc *.docx")])
    return filepath