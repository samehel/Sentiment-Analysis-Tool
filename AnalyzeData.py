import pandas as pd
import numpy as np
import html
import string
import nltk.data

class AnalyzeData:

    def __init__(self, dataset):
        self.dataset = dataset
    
    def InitAnalysis(self):
        self.__CleanData()
        return self.__ProcessData()

    def __CleanData(self):
        df = pd.read_csv(f'Datasets/{self.dataset}.csv')
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)

        def __RemovePunctuation(column):
            table = str.maketrans('', '', string.punctuation)
            return column.translate(table)

        def __CleanAirlineData(df):
            pass

        def __CleanGenericData(df):
            pass

        def __CleanIMDBData(df):
            df['review'] = df['review'].apply(lambda x: html.unescape(x))
            df['review'] = df['review'].str.replace('<br />', '')
            df['review'] = df['review'].str.replace('*', '')
            df['review'] = df['review'].apply(__RemovePunctuation)
            print(df)

        if self.dataset == "Airline Review Tweets":
            df = __CleanAirlineData(df)
        elif self.dataset == "Generic Sentiments":
            df = __CleanGenericData(df)
        elif self.dataset == "IMDB Dataset":
            df = __CleanIMDBData(df)
        
    def __ProcessData(self):
        pass