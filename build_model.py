import pandas as pd
import numpy as np
import ast
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

# Merge datasets
movies = movies.merge(credits, on='title')

# Select important columns
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

# Remove null values
movies.dropna(inplace=True)

# Convert string to list
def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert)

# Extract director
def fetch_director(text):
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            return i['name']
    return ""

movies['crew'] = movies['crew'].apply(fetch_director)

# Create tags column
movies['tags'] = movies['overview'] + " " + \
                 movies['genres'].astype(str) + " " + \
                 movies['keywords'].astype(str) + " " + \
                 movies['cast'].astype(str) + " " + \
                 movies['crew']

# Convert text to vectors
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

# Calculate cosine similarity
similarity = cosine_similarity(vectors)

# Save files
pickle.dump(movies, open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("Model built successfully ✅")