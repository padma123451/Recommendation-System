
import os
import numpy as np
import pandas as pd
import ast
import warnings
warnings.filterwarnings("ignore")
os.getcwd()


movies = pd.read_csv("movies.csv")
credits = pd.read_csv("credits.csv")



movies = movies.merge(credits, on='title')
movies['original_language'].value_counts(normalize=True)
movies = movies[['genres','keywords', 'overview','title','cast', 'crew']]



def convert(text):
    return [i["name"] for i in ast.literal_eval(text)]

def convert1(text):
    return [i["name"] for i in ast.literal_eval(text)[:5]]
    

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert1)



def fetch_director(text):
    ext2 = []
    for i in ast.literal_eval(text):
        if i['job']=='Director':
            ext2.append(i['name'])
    return ext2

# %%
movies['crew'] = movies['crew'].apply(fetch_director)
movies.dropna(inplace=True)

def collapse(ext):
    ext4 = []
    for i in ext:
        ext4.append(i.replace(" ",""))
    return ext4


movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)
movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)


movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies['context'] = movies['genres'] + movies['keywords'] + movies['overview'] + movies['cast'] + movies['crew']
new = movies.drop(columns=['genres', 'keywords', 'overview', 'cast', 'crew'], axis=1)
new['context'] = new['context'].apply(lambda x: " ".join(x))


from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')
vector = cv.fit_transform(new['context']).toarray()
vector.shape


from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vector)
similarity



def recommend(movie_name):
    movie_index = new[new['title']==movie_name].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key= lambda x: x[1])
    recommend_movies = []
    for i in movies_list[1:6]:
        recommend_movies.append(new.iloc[i[0]].title)

    return recommend_movies













