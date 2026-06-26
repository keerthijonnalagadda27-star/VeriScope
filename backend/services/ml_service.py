import joblib

classifier=joblib.load('model/classifier.joblib')
vectorizer=joblib.load('model/vectorizer.joblib')

def predict(text) :
    text_tfidf=vectorizer.transform([text])
    prediction=classifier.predict(text_tfidf)[0]
    probability=classifier.predict_proba(text_tfidf)[0]
    
    verdict="REAL" if prediction==1 else "FAKE"
    confidence=round(float(max(probability))*100,2)

    return {
        "verdict":verdict,
        "confidence":confidence,
        "fake_probability":round(float(probability[0])*100,2),
        "real_probability":round(float(probability[1])*100,2)
    }


