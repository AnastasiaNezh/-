import pandas as pd
import joblib
import spacy
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

nlp = spacy.load("ru_core_news_md")

def get_vector(text):
    return nlp(str(text).lower()).vector

df = pd.read_csv("dataset.csv")

X = np.array([get_vector(text) for text in df['text']])
y = df['intent']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

print(f"Модель обучена. Точность: {model.score(X_test, y_test)}")

joblib.dump(model, 'intent_model.pkl')