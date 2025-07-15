import pickle
import streamlit as st
import requests
import pandas as pd
from urllib.parse import quote_plus


# --- Fetch Poster ---
def fetch_poster_by_title(title):
    api_key = "My Api key"
    url = f"http://www.omdbapi.com/?t={quote_plus(title)}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    poster_url = data.get('Poster')
    if poster_url and poster_url != "N/A":
        return poster_url
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"


# --- Recommend Function ---
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        title = movies.iloc[i[0]].title
        recommended_movie_names.append(title)
        recommended_movie_posters.append(fetch_poster_by_title(title))

    return recommended_movie_names, recommended_movie_posters


# --- Load Data ---
movies = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Streamlit Config ---
st.set_page_config(page_title="Movie Recommender", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: white;
        }
        .title {
            text-align: center;
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #a3d3ff;
        }
        .stButton > button {
            background-color: #ff4b4b;
            color: white;
            padding: 0.6em 1.5em;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #ff6f6f;
        }
        .movie-title {
            font-size: 1rem;
            text-align: center;
            padding-top: 0.5rem;
            color: #e0e0e0;
        }
        img {
            border-radius: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# --- UI Title ---
st.markdown('<div class="title">🎬 Movie Recommender System</div>', unsafe_allow_html=True)

# --- Movie Selection ---
selected_movie = st.selectbox("Type or select a movie from the dropdown", movies['title'].values)

# --- Button & Output ---
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(f"<div class='movie-title'>{recommended_movie_names[i]}</div>", unsafe_allow_html=True)
            st.image(recommended_movie_posters[i], use_container_width=True)

