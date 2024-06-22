import pandas as pd
import html
import string
import nltk

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm  
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

class AnalyzeData:

    def __init__(self, dataset):
        self.dataset = dataset
        self.__CheckNLTKDirectories()
        self.lemmatizer = WordNetLemmatizer()
        self.stopWords = set(stopwords.words('english'))
        self.TFIDFVectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
        self.model = LogisticRegression(max_iter=1000)

    def __CheckNLTKDirectories(self):
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('stopwords')
            nltk.data.find('wordnet')
            print("Directories already exist.")
        except LookupError:
            print("Directories not found. Downloading now...")
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('wordnet')
            print("Download Complete.")

    def InitAnalysis(self):
        PreProcessedData = self.__CleanAndPreProcessData()
        return self.__ProcessData(PreProcessedData=PreProcessedData)

    def __CleanAndPreProcessData(self):
        print('Now cleaning data...')
        df = pd.read_csv(f'Datasets/{self.dataset}.csv')
        df.drop_duplicates(inplace=True)

        def __RemovePunctuation(column):
            table = str.maketrans('', '', string.punctuation)
            return column.translate(table)

        def LemmatizeTokens(tokens):
            return [self.lemmatizer.lemmatize(word) for word in tokens]

        def __CleanData(df, textColumn):

            tqdm.pandas(desc="Cleaning html elements and converting text to lowercase")
            df[textColumn] = df[textColumn].progress_apply(lambda x: html.unescape(x))
            df[textColumn] = df[textColumn].str.replace('<br />', '')
            df[textColumn] = df[textColumn].str.replace('*', '')
            df[textColumn] = df[textColumn].str.replace(r'@([A-Za-z0-9_]+)', '')
            df[textColumn] = df[textColumn].str.lower()
            
            tqdm.pandas(desc="Removing Punctuation")
            df[textColumn] = df[textColumn].progress_apply(__RemovePunctuation)
            
            tqdm.pandas(desc="Tokenizing")
            df['tokens'] = df[textColumn].progress_apply(word_tokenize)
            
            tqdm.pandas(desc="Removing Stopwords") 
            df['tokens'] = df['tokens'].progress_apply(lambda x: [word for word in x if word not in self.stopWords])
            
            tqdm.pandas(desc="Lemmatizing")
            df['tokens'] = df['tokens'].progress_apply(LemmatizeTokens)
            
            tqdm.pandas(desc="Joining Tokens")
            df[textColumn] = df['tokens'].progress_apply(lambda tokens: ' '.join(tokens))

            return df

        def __PreProcessData(X, y):
            print('Now pre-processing data...')

            X = X.apply(lambda tokens: ' '.join(tokens) if isinstance(tokens, list) else tokens)

            X_tfidf = self.TFIDFVectorizer.fit_transform(X)
            print("Vocabulary size: ", len(self.TFIDFVectorizer.vocabulary_))
            print("Features: ", len(self.TFIDFVectorizer.get_feature_names_out()))

            print('Now training model...')
            X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.3, random_state=42)
            self.model.fit(X_train, y_train)
            accuracy = self.model.score(X_test, y_test)
            print(f'Training Accuracy: {accuracy * 100:.2f}%')

            return {
                "Training_Accuracy": accuracy,
                "X_test": X_test,
                "y_test": y_test,
                "Class_Labels": y.unique()
            }
                   
        if self.dataset == "Airline Review Tweets":
            df = __CleanData(df, 'text')
            PreProcessedData = __PreProcessData(df['text'], df['airline_sentiment'])
            return PreProcessedData
        elif self.dataset == "Generic Sentiments":
            df.dropna(inplace=True)
            df = __CleanData(df, 'text')
            PreProcessedData = __PreProcessData(df['text'], df['sentiment'])
            return PreProcessedData
        elif self.dataset == "IMDB Dataset":
            df = __CleanData(df, 'review')
            PreProcessedData = __PreProcessData(df['review'], df['sentiment'])
            return PreProcessedData

    def __ProcessData(self, PreProcessedData):
        y_pred = self.model.predict(PreProcessedData["X_test"])
        accuracy = accuracy_score(PreProcessedData["y_test"], y_pred)
        print(f'Evaluation Accuracy: {accuracy * 100:.2f}%')
        print("Classification Report")
        classificationReport = classification_report(PreProcessedData["y_test"], y_pred)
        print(classificationReport)
        print("Confusion Matrix")
        confusionMatrix = confusion_matrix(PreProcessedData["y_test"], y_pred)
        print(confusionMatrix)
        
        return {
            "Training_Accuracy" : PreProcessedData["Training_Accuracy"],
            "Class_Labels": PreProcessedData["Class_Labels"],
            "Evaluation_Accuracy" : accuracy,
            "Classification_Report": classificationReport,
            "Confusion_Matrix": confusionMatrix
        }