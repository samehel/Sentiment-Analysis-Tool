import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np

from tkinter import ttk
from AnalyzeData import AnalyzeData
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GUI:

    def __init__(self, root):
        self.dataset = None
        self.SelectDatasetWindow = None
        self.ErrorPopup = None
        self.DisplayDataWindow = None

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

        if self.DisplayDataWindow is not None:
            self.DisplayDataWindow.destroy()

        DisplayDataWindow = tk.Toplevel(self.root)
        DisplayDataWindow.title("Sentiment Analysis Tool")
        DisplayDataWindow.geometry("800x1000")
        DisplayDataWindow.resizable(False, False)

        self.DisplayDataWindow = DisplayDataWindow

        ttk.Label(DisplayDataWindow, text=f"Testing Accuracy: {AnalyzedData["Training_Accuracy"]* 100:.2f}%", style="Heading.TLabel").pack(pady=10)
        ttk.Label(DisplayDataWindow, text=f"Evaluation Accuracy: {AnalyzedData["Evaluation_Accuracy"]* 100:.2f}%", style="Heading.TLabel").pack(pady=10)

        ttk.Label(DisplayDataWindow, text="Classification Report", style="Heading.TLabel").pack(pady=10)
        
        ClassificationReportText = tk.Text(DisplayDataWindow, height=10, width=60)
        ClassificationReportText.insert(tk.END, AnalyzedData["Classification_Report"])
        ClassificationReportText.config(state=tk.DISABLED)
        ClassificationReportText.pack()

        fig, ax = plt.subplots()
        cax = ax.matshow(AnalyzedData["Confusion_Matrix"], cmap='Blues')
        fig.colorbar(cax)

        for (i, j), val in np.ndenumerate(AnalyzedData["Confusion_Matrix"]):
            ax.text(j, i, f'{val}', ha='center', va='center')

        ax.set_xlabel('Predicted')
        ax.set_ylabel('Actual')
        ax.set_xticks(range(len(AnalyzedData["Class_Labels"])))
        ax.set_yticks(range(len(AnalyzedData["Class_Labels"])))
        ax.set_xticklabels(AnalyzedData["Class_Labels"])
        ax.set_yticklabels(AnalyzedData["Class_Labels"])
        plt.title('Confusion Matrix')

        plt.tight_layout() 

        canvas = FigureCanvasTkAgg(fig, master=DisplayDataWindow)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)
        
        ttk.Button(DisplayDataWindow, text="Close", command=DisplayDataWindow.destroy, style="TButton").pack(pady=10)

    def __ExitProgram(self):
        self.root.destroy()
        exit()


        