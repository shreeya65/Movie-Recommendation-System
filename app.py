import streamlit as st
import pandas as pd
import pickle as pk
import requests
movies_list = pk.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_list)
similarity = pk.load(open('similarity.pkl','rb'))

def fetch(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommended = []
    poster_path = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended.append(movies.iloc[i[0]].title)
        poster_path.append(fetch(movie_id))
    return recommended,poster_path

st.title('Movie Recommender')

option = st.selectbox(
    "Which of the following movie you like the most?", movies['title'].values,
        placeholder='Select Movie')

st.write("You selected:", option)
selected_movie = option
if st.button('Recommend'):
    recommendations,posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(posters[0])
    with col2:
        st.text(recommendations[1])
        st.image(posters[1])

    with col3:
        st.text(recommendations[2])
        st.image(posters[2])
    with col4:
        st.text(recommendations[3])
        st.image(posters[3])
    with col5:
        st.text(recommendations[4])
        st.image(posters[4])

