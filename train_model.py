from pathlib import Path
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "dataset" / "enron_spam_data.csv"
MODEL_DIR = BASE_DIR / "model"

MODEL_DIR.mkdir(exist_ok=True)

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully.")
print("Number of emails:", len(df))
print("Columns:", list(df.columns))

df["Subject"] = df["Subject"].fillna("")
df["Message"] = df["Message"].fillna("")

df["text"] = df["Subject"] + " " + df["Message"]

df["label"] = df["Spam/Ham"].map({
    "ham": 0,
    "spam": 1
})

df = df.dropna(subset=["label"])

X = df["text"]
y = df["label"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training model...")

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            min_df=1
        )
    ),
    (
        "classifier",
        LogisticRegression(max_iter=2000)
    )
])

model.fit(X_train, y_train)

print("Model training completed.")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Legitimate", "Spam"]
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

model_path = MODEL_DIR / "spam_model.pkl"

joblib.dump(model, model_path)

print("\nModel saved successfully!")
print("Saved at:", model_path)