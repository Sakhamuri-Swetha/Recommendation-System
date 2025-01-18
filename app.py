import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

image = "images/movie-poster.jpg"
st.set_page_config(
    page_title="K-Drama Recommendation App",
    page_icon=":tv:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://res.cloudinary.com/jerrick/image/upload/v1674914907/63d52c5b117749001de8b595.png" 
             alt="K-Drama Screenshot" 
             style="width: 450px; height: auto; object-fit: contain; margin-bottom: 35px;">
        <h1 style="color: #F98B88; margin-bottom: 30px;">K-Drama Recommendation System</h1>
    </div>
    """,
    unsafe_allow_html=True
)

data = pd.read_csv('kdrama_cleaned_dataset.csv')
data['Combined_Features'] = (
    data['Genre'].fillna('') + ' ' +
    data['Actors'].fillna('') + ' ' +
    data['Directors'].fillna('') + ' ' +
    data['Plot'].fillna('')
)

tfidf = TfidfVectorizer(stop_words='english')
vectorized_features = tfidf.fit_transform(data['Combined_Features'])
similarity_matrix = cosine_similarity(vectorized_features)
def recommend_kdramas(title, top_n=25):
    if title not in data['Title'].values:
        return []
    
    idx = data[data['Title'] == title].index[0]
    similarity_scores = list(enumerate(similarity_matrix[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    top_kdramas = []
    for i in similarity_scores[1:top_n+1]:
        drama_title = data.iloc[i[0]]['Title']
        poster_url = data.iloc[i[0]]['Poster_Image']
        
        if pd.isna(poster_url) or poster_url == "No image" or not poster_url.startswith("http"):
            poster_url = "https://github.com/Sakhamuri-Swetha/Recommendation-System/blob/main/images/IMG1.png?raw=true"

        official_site = data.iloc[i[0]]['Link'] if 'Link' in data.columns else '#'
        actors = data.iloc[i[0]]['Actors'] if 'Actors' in data.columns else 'Unknown'
        actors_list = actors.strip("[]").replace("'", "").split(",")
        actors = ", ".join(actors_list)
        genre = data.iloc[i[0]]['Genre'] if 'Genre' in data.columns else 'Unknown Genre'
        genre_list = genre.strip("[]").replace("'", "").split(",")
        genre = ", ".join(genre_list)
        
        rating = data.iloc[i[0]]['IMDb_Rating'] if 'IMDb_Rating' in data.columns else 'N/A'
        summary = data.iloc[i[0]]['Plot'][:100]  
        top_kdramas.append((drama_title, poster_url, actors, genre, rating, summary, official_site))
    return top_kdramas

search_term = st.text_input('Enter the title of a K-Drama to get recommendations:')

if search_term:
    filtered_titles = [title for title in data['Title'] if search_term.lower() in title.lower()]
    if filtered_titles:
        selected_title = st.selectbox('Select a K-Drama:', filtered_titles)
        recommendations = recommend_kdramas(selected_title)
        if recommendations:
            st.markdown(f"### Recommendations based on '{selected_title}':")
            num_rows = 5
            num_cols = 5
            with st.container():
                for row in range(num_rows):
                    cols = st.columns(num_cols)
                    for col, (drama_name, poster_url, actors, genre, rating, summary, official_site) in zip(cols, recommendations[row * num_cols:(row + 1) * num_cols]):
                        with col:
                            
                            st.markdown(
                                    f"""
                                    <div style="text-align: center; margin-bottom: 20px; font-family: 'Garamond', Serif;">
                                        <img src="{poster_url}" alt="{drama_name}" style="width: 200px; height: 300px; object-fit: cover;"/>
                                        <p style="color: #C0C0C0; font-size: 18px; font-weight: bold; margin: 0; padding: 0; line-height: 1.2;">{drama_name}</p>
                                        <p style="color: #C0C0C0; font-size: 14px; margin: 0; padding: 0; line-height: 1.2;"><strong>Genre:</strong> {genre}</p>
                                        <p style="color: #C0C0C0; font-size: 14px; margin: 0; padding: 0; line-height: 1.2;"><strong>Rating:</strong> {rating}</p>
                                        <p style="color: #C0C0C0; font-size: 14px; margin: 0; padding: 0; line-height: 1.2;"><strong>Summary:</strong> {summary}... 
                                            <a href="{official_site}" target="_blank" style="color: #FF6347; text-decoration: none;">Read More</a>
                                        </p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )


    else:
        st.write("No titles found matching your search.")
