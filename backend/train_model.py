import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,classification_report
import joblib

fake=pd.read_csv("data/Fake.csv")
true=pd.read_csv("data/True.csv")
fake['label']=0
true['label']=1
df = pd.concat([fake, true], ignore_index=True)
df=df.sample(frac=1,random_state=42).reset_index(drop=True)
#ikkada drop=true ante paatha scrambled index throw chesesey and dont store it as a new column ani ardam
df["title"] = df["title"].fillna("")
df["text"] = df["text"].fillna("")
df["content"] = df["title"] + " " + df["text"]

X_train,X_test,y_train,y_test=train_test_split(
    df['content'],
    df['label'],
    test_size=0.2,
    random_state=42
)


vectorizer=TfidfVectorizer()
X_train_tfidf=vectorizer.fit_transform(X_train)

X_test_tfidf=vectorizer.transform(X_test)

lr=LogisticRegression(max_iter=1000)

lr.fit(X_train_tfidf,y_train)

y_pred=lr.predict(X_test_tfidf)
print(f"Accuracy:{accuracy_score(y_test,y_pred):.4f}")
print(classification_report(y_test,y_pred,target_names=['Fake','Real']))

joblib.dump(lr, 'model/classifier.joblib')
joblib.dump(vectorizer, 'model/vectorizer.joblib')
