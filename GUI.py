import tkinter as tk

from tkinter import ttk
from AnalyzeData import AnalyzeData

class GUI:

    def __init__(self, root):
        self.dataset = None
        self.SelectDatasetWindow = None
        self.ErrorPopup = None

        self.root = root
        self.root.title("Sentiment Analysis Tool")
        self.root.geometry("315x350")
        self.root.resizable(False, False)

        self.style = ttk.Style(root)
        self.style.configure('TLabel', font=("Helvetica", 12), padding=10)
        self.style.configure('TButton', font=("Helvetica", 10), padding=10)
        self.style.configure('Heading.TLabel', font=("Helvetica", 10, "bold"), padding=10)
        self.style.configure('Error.TLabel', font=("Helvetica", 10, "bold"), padding=10, foreground="red")

        self.title = ttk.Label(root, text="Choose an Option", style="Heading.TLabel")
        self.title.pack(pady=10)
        
        self.datasetSelected = ttk.Label(root, text="Selected Dataset: " + str(self.dataset), style="TLabel")
        self.datasetSelected.pack(pady=10)

        self.selectButton = ttk.Button(root, text="Select Dataset", command=self.__SelectDataset, style="TButton")
        self.selectButton.pack(pady=10)

        self.runAnalysis = ttk.Button(root, text="Analyze Data", command=self.__AnalyzeAndDisplayData, style="TButton")
        self.runAnalysis.pack(pady=10)

        self.exitButton = ttk.Button(root, text="Exit", command=self.__ExitProgram, style="TButton")
        self.exitButton.pack(pady=10)

    def __SelectDataset(self):
        if self.SelectDatasetWindow is not None:
            self.SelectDatasetWindow.destroy()

        options = ["Generic Sentiments", "IMDB Dataset", "Airline Review Tweets"]
        selected = tk.StringVar()
        selected.set(options[0])

        def __onSelect():
            self.dataset = selected.get()
            SelectDatasetWindow.destroy()
            self.__RefreshMainMenu()

        def __onCancel():
            SelectDatasetWindow.destroy()

        SelectDatasetWindow = tk.Toplevel(self.root)
        SelectDatasetWindow.title("Sentiment Analysis Tool")
        SelectDatasetWindow.geometry("290x300")
        SelectDatasetWindow.resizable(False, False)

        self.SelectDatasetWindow = SelectDatasetWindow

        ttk.Label(SelectDatasetWindow, text="Choose a Dataset", style="Heading.TLabel").pack(pady=10)

        for option in options:
            ttk.Radiobutton(SelectDatasetWindow, text=option, variable=selected, value=option).pack(anchor=tk.W)

        ttk.Button(SelectDatasetWindow, text="Confirm Selection", command=__onSelect).pack(pady=10)
        ttk.Button(SelectDatasetWindow, text="Cancel", command=__onCancel).pack(pady=10)

        self.root.wait_window(SelectDatasetWindow)
        return getattr(self, 'dataset', None)
    
    def __RefreshMainMenu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.title = ttk.Label(self.root, text="Choose an Option", style="Heading.TLabel")
        self.title.pack(pady=10)
        
        self.datasetSelected = ttk.Label(self.root, text=f"Selected Dataset: {str(self.dataset)}", style="TLabel")
        self.datasetSelected.pack(pady=10)

        self.selectButton = ttk.Button(self.root, text="Select Dataset", command=self.__SelectDataset, style="TButton")
        self.selectButton.pack(pady=10)

        self.runAnalysis = ttk.Button(self.root, text="Analyze Data", command=self.__AnalyzeAndDisplayData, style="TButton")
        self.runAnalysis.pack(pady=10)

        self.exitButton = ttk.Button(self.root, text="Exit", command=self.__ExitProgram, style="TButton")
        self.exitButton.pack(pady=10)

    def __AnalyzeAndDisplayData(self):
        if self.dataset == None:
            if self.ErrorPopup is not None:
                self.ErrorPopup.destroy()

            ErrorPopup = tk.Toplevel(self.root)
            ErrorPopup.title("Sentiment Analysis Tool")
            ErrorPopup.geometry("290x50")
            ErrorPopup.resizable(False, False)

            self.ErrorPopup = ErrorPopup

            ttk.Label(ErrorPopup, text="Error: Please select a dataset first.", style="Error.TLabel").pack(pady=10)
            return
        
        AnalyzedData = AnalyzeData(self.dataset)
        AnalyzedData = AnalyzedData.InitAnalysis()


    def __ExitProgram(self):
        self.root.destroy()


        