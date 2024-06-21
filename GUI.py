import tkinter as tk

from tkinter import messagebox
from tkinter import ttk

class GUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Sentiment Analysis Tool")
        self.root.geometry("315x150")
        self.root.resizable(False, False)

        self.style = ttk.Style(root)
        self.style.configure('TLabel', font=("Helvetica", 12), padding=10)
        self.style.configure('TButton', font=("Helvetica", 10), padding=10)

        self.title = ttk.Label(root, text="Choose an Option", style="TLabel")

        self.selectButton = ttk.Button(root, text="Select Dataset", command=self.SelectDataset, style="TButton")
        self.selectButton.pack(pady=10)
        

        self.exitButton = ttk.Button(root, text="Exit", command=self.ExitProgram, style="TButton")
        self.exitButton.pack(pady=10)

        self.dataset = None

    def SelectDataset(self):
        options = ["Generic Sentiments", "IMBD Dataset", "Airline Review Tweets", "Upload your own dataset"]
        selected = tk.StringVar()
        selected.set(options[0])

        def onSelect():
            self.dataset = selected.get()
            SelectDatasetWindow.destroy()

        def onCancel():
            SelectDatasetWindow.destroy()

        SelectDatasetWindow = tk.Toplevel(self.root)
        SelectDatasetWindow.title("Sentiment Analysis Tool")
        SelectDatasetWindow.geometry("290x300")
        SelectDatasetWindow.resizable(False, False)

        ttk.Label(SelectDatasetWindow, text="Choose a Dataset", font="Bold").pack(pady=10)

        for option in options:
            ttk.Radiobutton(SelectDatasetWindow, text=option, variable=selected, value=option).pack(anchor=tk.W)

        ttk.Button(SelectDatasetWindow, text="Confirm Selection", command=onSelect).pack(pady=10)
        ttk.Button(SelectDatasetWindow, text="Cancel", command=onCancel).pack(pady=10)

        self.root.wait_window(SelectDatasetWindow)
        return getattr(self, 'dataset', None)
    
    def ExitProgram(self):
        self.root.destroy()


        