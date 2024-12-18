from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer

# Load the GoEmotions dataset
ds = load_dataset("google-research-datasets/go_emotions", "simplified")
mlb = MultiLabelBinarizer()

X_train = ds["train"]["text"]
y_train = mlb.fit_transform(ds["train"]["labels"])
X_dev = ds["validation"]["text"]
y_dev = mlb.fit_transform(ds["validation"]["labels"])
X_test = ds["test"]["text"]
y_test = mlb.fit_transform(ds["test"]["labels"])

# Convert the text data to TF-IDF features
tfidf = TfidfVectorizer(max_features=5000, stop_words="english")
X_train_tfidf = tfidf.fit_transform(X_train)
X_dev_tfidf = tfidf.transform(X_dev)
X_test_tfidf = tfidf.transform(X_test)

# Train a Logistic Regression model
model = OneVsRestClassifier(LogisticRegression(max_iter=1000))
model.fit(X_train_tfidf, y_train)

# Evaluate on the training set
y_train_pred = model.predict(X_train_tfidf)
print("Training Set Accuracy:", accuracy_score(y_train, y_train_pred))
print(
    "Training Set Classification Report:\n",
    classification_report(y_train, y_train_pred, zero_division=0),
)

# Evaluate on the development set
y_dev_pred = model.predict(X_dev_tfidf)
print("Development Set Accuracy:", accuracy_score(y_dev, y_dev_pred))
print(
    "Development Set Classification Report:\n",
    classification_report(y_dev, y_dev_pred, zero_division=0),
)

# Evaluate on the test set
y_test_pred = model.predict(X_test_tfidf)
print("Test Set Accuracy:", accuracy_score(y_test, y_test_pred))
print(
    "Test Set Classification Report:\n",
    classification_report(y_test, y_test_pred, zero_division=0),
)
