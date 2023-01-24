import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests

def fetch_poster(movie_id):

    response= requests.get("https://api.themoviedb.org/3/movie/{}?api_key=e53cf988fdc7a11f4690e45902b88df5".format(movie_id))
    data= response.json()
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']

def recommend(movie, movies_list):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    movie_id= movies_list[movies_list['title'] == movie]['movie_id']
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_movie_posters=[]
    for i in movies_list:
        id= movies_df.iloc[i[0]].movie_id
        recommended_movies.append(i[0])
        #fetching poster from API
        recommended_movie_posters.append(fetch_poster(id))

    return recommended_movies,recommended_movie_posters

movies_df= pickle.load(open('movie.pkl','rb'))
similarity= pickle.load(open('similarity.pkl','rb'))

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'What movie would you like to watch?',
    movies_df['title'].values)


if st.button('Search similar movies'):
    movie,posters= recommend(selected_movie_name,movies_df)

    for i in movie:
        st.write(movies_df['title'].iloc[i])
    # st.write(posters)
    col1, col2, col3,col4, col5 = st.columns(5)

    with col1:
        st.header(movies_df['title'].iloc[movie[0]])
        st.image(posters[0])
    with col2:
        st.header(movies_df['title'].iloc[movie[1]])
        st.image(posters[1])
    with col3:
        st.header(movies_df['title'].iloc[movie[2]])
        st.image(posters[2])
    with col4:
        st.header(movies_df['title'].iloc[movie[3]])
        st.image(posters[3])
    with col5:
        st.header(movies_df['title'].iloc[movie[4]])
        st.image(posters[4])

# else:
#     st.write('Goodbye')
