import pandas as pd
import joblib
import spacy
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load("ru_core_news_sm")

def preprocess(text):
    doc = nlp(str(text).lower())
    return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

df = pd.read_csv("dataset.csv")
X = df['text'].apply(preprocess)
y = df['intent']

vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y, test_size=0.2, random_state=1
)

model = LogisticRegression()
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Модель обучена. Точность: {accuracy}")

joblib.dump(model, 'intent_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')