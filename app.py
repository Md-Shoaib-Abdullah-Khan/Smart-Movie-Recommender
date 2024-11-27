import pandas as pd
import requests
import streamlit as st
import pickle

st.title('Movie Recommender Sytem')

import streamlit as st

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:21]
    recommended = []
    recommended_movie_poseters = []

    for i in movies_list:
        recommended.append(movies.iloc[i[0]].title)
        recommended_movie_poseters.append(fetch_poster(movies.iloc[i[0]].movie_id))

    return recommended, recommended_movie_poseters
def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=934c65db2d7807dce6329330ba401ba8&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']



selected_movie = st.selectbox(
    "What type of movie would you like to be recommended?",
    movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    row1 = st.columns(5)
    row2 = st.columns(5)
    row3 = st.columns(5)
    row4 = st.columns(5)

    for col,i in zip((row1 + row2 + row3 + row4), range(20)):
        with col:
            st.text(names[i])
            st.image(posters[i])

