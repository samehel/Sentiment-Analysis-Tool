# Sentiment Analysis Tool

This Python application performs sentiment analysis on different datasets using Natural Language Processing (NLP) techniques and provides a graphical user interface (GUI) for interaction.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [File Structure](#file-structure)

## Introduction

This tool uses a Logistic Regression model trained on TF-IDF vectorized text data to classify sentiments from various datasets. It includes functionalities for data cleaning, preprocessing, model training, and evaluation. The graphical interface allows users to select a dataset, analyze sentiment, and visualize results using a confusion matrix and classification report.

## Features

- **Dataset Selection:** Choose from three datasets: Generic Sentiments, IMDB Dataset, and Airline Review Tweets.
- **Data Cleaning and Preprocessing:** Remove duplicates, handle missing values, clean HTML elements, lowercase text, remove punctuation, tokenize, remove stopwords, and lemmatize.
- **Model Training:** Train a Logistic Regression model using TF-IDF vectorization.
- **Evaluation:** Display training and evaluation accuracies, classification report, and confusion matrix.
- **GUI:** Simple and intuitive graphical user interface for dataset selection and result display.
- **Visualization:** Display confusion matrix with labels and classification report in a text box.

## Requirements

- Python 3.x
- Libraries:
  - pandas
  - numpy
  - nltk
  - scikit-learn
  - tqdm
  - tkinter (for GUI)
  - matplotlib

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/samehel/Sentiment-Analysis-Tool.git
   cd repository
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Program:**
   ```bash
   python Main.py
   ```
   - Select a dataset and confirm your selection.
   - Click on "Analyze Data" to start sentiment analysis.
   - Results (accuracy, classification report, confusion matrix) will be displayed in a new window.

2. **Interact with the GUI:**
   - **Select Dataset:** Choose between "Generic Sentiments", "IMDB Dataset", and "Airline Review Tweets".
   - **Analyze Data:** Initiates data preprocessing, model training, and displays analysis results.
   - **Exit:** Closes the application.

## File Structure

- **AnalyzeData.py:** Contains the `AnalyzeData` class for data preprocessing, model training, and evaluation.
- **GUI.py:** Implements the graphical user interface using tkinter for dataset selection and result visualization.
- **Datasets/:** Directory containing CSV files of the datasets used for sentiment analysis.

```
repository/
│
├── AnalyzeData.py
├── GUI.py
├── Datasets/
│   ├── Generic Sentiments.csv
│   ├── IMDB Dataset.csv
│   └── Airline Review Tweets.csv
├── README.md
└── requirements.txt
```
