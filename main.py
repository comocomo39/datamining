import pandas as pd
import ast
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

def safe_extract_first_genre(genres_str):
    try:
        genres_list = ast.literal_eval(genres_str)
        if genres_list:
            return genres_list[0]
    except:
        pass
    return 'Unknown'

# Caricamento dei dati
file_path = 'C:/Users/casac/Downloads/movie_data.csv/movie_data.csv'
df = pd.read_csv(file_path, engine='python', on_bad_lines='skip')
df['first_genre'] = df['genres'].apply(safe_extract_first_genre)
genres_of_interest = ['Horror', 'Action', 'Drama', 'Comedy']
df_filtered = df[df['first_genre'].isin(genres_of_interest)]

# Bilanciamento delle classi
min_count = df_filtered['first_genre'].value_counts().min()
df_balanced = pd.DataFrame()
for genre in genres_of_interest:
    df_genre = df_filtered[df_filtered['first_genre'] == genre].sample(n=min_count, random_state=42)
    df_balanced = pd.concat([df_balanced, df_genre])

# Preprocessing e divisione del dataset
X = df_balanced['overview'].fillna('')
y = df_balanced['first_genre']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline per TfidfVectorizer + SVM
pipeline_svm = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', ngram_range=(1,2))),
    ('svm', SVC(kernel='linear'))
])

# Addestramento e valutazione SVM
pipeline_svm.fit(X_train, y_train)
svm_predictions = pipeline_svm.predict(X_test)
print(f'SVM Accuracy: {accuracy_score(y_test, svm_predictions)}')

# 1. Estrai il modello SVM e il TfidfVectorizer dalla pipeline
svm_model = pipeline_svm.named_steps['svm']
vectorizer = pipeline_svm.named_steps['tfidf']

# 2. Ottieni i coefficienti dal modello SVM
coefficients = svm_model.coef_.toarray()  # Converte da sparse a dense se necessario

# 3. Ottieni i nomi delle caratteristiche (termini) dal TfidfVectorizer
feature_names = vectorizer.get_feature_names_out()

# 4. Associa ciascun peso ai rispettivi nomi delle caratteristiche e ordina per importanza
feature_importance = zip(feature_names, coefficients[0])
sorted_features = sorted(feature_importance, key=lambda x: x[1], reverse=True)

# 5. Stampa le prime N caratteristiche più importanti
N = 10  # Numero di caratteristiche da visualizzare
print("Top 10 important features:")
for feature, weight in sorted_features[:N]:
    print(f"{feature}: {weight}")

import joblib

# Salvare la pipeline addestrata
joblib.dump(pipeline_svm, 'svm_pipeline.joblib')
