python -m pip install scikit-learn
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
# Load the CSV file
df = pd.read_csv('GoogleReview_data_cleaned.csv')

# Ensure only relevant columns are kept and handle missing values
df = df[['Author', 'Rating', 'Restaurant', 'Location']].dropna()

# Convert rating to numeric
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

# Create a pivot table with users as rows and restaurants as columns
user_item_matrix = df.pivot_table(index='Author', columns='Restaurant', values='Rating').fillna(0)

# Compute item (restaurant) similarity
restaurant_similarity = cosine_similarity(user_item_matrix.T)
restaurant_similarity_df = pd.DataFrame(restaurant_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)

# Function to get similar restaurants for a given restaurant
def get_similar_restaurants(restaurant, top_n=3):
    similar_restaurants = restaurant_similarity_df[restaurant].sort_values(ascending=False)[1:top_n+1]
    return similar_restaurants

# Streamlit app structure
st.set_page_config(page_title="Restaurant Recommendation System", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    body {
        background-color: #f0f0f5;
        font-family: 'Arial', sans-serif;
    }
    .main-header {
        text-align: center;
        color: #ff6600;
    }
    .recommendation-section {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 12px #aaaaaa;
    }
    .recommend-button {
        background-color: #ff6600;
        color: white;
        padding: 10px 15px;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }
    .recommend-button:hover {
        background-color: #e65c00;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Restaurant Recommendation System")

# Allow users to rate a restaurant
selected_restaurant = st.selectbox("Select a restaurant to rate:", user_item_matrix.columns)
user_rating = st.slider("Rate this restaurant (1-5):", 1, 5, 3)
submit_rating = st.button("Submit Rating")

if submit_rating:
    # Let's assume the current user is 'New_User' (for demo purposes)
    user = 'New_User'

    # If the user is new, add them to the user-item matrix
    if user not in user_item_matrix.index:
        user_item_matrix.loc[user] = 0

    # Update the user's rating for the selected restaurant
    user_item_matrix.loc[user, selected_restaurant] = user_rating

    st.write(f"Thank you for rating {selected_restaurant}!")

    # Recompute the restaurant similarity matrix after adding new ratings
    restaurant_similarity = cosine_similarity(user_item_matrix.T)
    restaurant_similarity_df = pd.DataFrame(restaurant_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)

    # Recommend similar restaurants based on the newly rated restaurant
    st.write("Based on your rating, we recommend these similar restaurants:")
    similar_restaurants = get_similar_restaurants(selected_restaurant, top_n=3)
    st.write(similar_restaurants)

# Display recommendations for an existing user
st.write("Alternatively, get recommendations based on your existing ratings:")

# Select user for recommendations
selected_user = st.selectbox("Select a user:", user_item_matrix.index)

# Choose system type: User-based or Item-based
system_type = st.radio("Choose Recommendation Type:", ('User-Based', 'Item-Based'))

if system_type == 'User-Based':
    # Compute user similarity
    user_similarity = cosine_similarity(user_item_matrix)
    user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

    # Function to get top similar users for a given user
    def get_similar_users(user, top_n=3):
        similar_users = user_similarity_df[user].sort_values(ascending=False)[1:top_n+1]
        return similar_users

    # Recommend restaurants for a user based on similar users
    def recommend_restaurants_for_user(user, top_n=3):
        similar_users = get_similar_users(user, top_n=top_n)
        similar_users_ratings = user_item_matrix.loc[similar_users.index]
        restaurant_recommendations = similar_users_ratings.mean().sort_values(ascending=False)
        user_rated_restaurants = user_item_matrix.loc[user]
        restaurant_recommendations = restaurant_recommendations[user_rated_restaurants == 0]
        return restaurant_recommendations.head(top_n)

    if st.button("Recommend Restaurants", key='user_rec_button'):
        user_recommendations = recommend_restaurants_for_user(selected_user)
        st.write(f"Top restaurant recommendations for user {selected_user}:")
        st.write(user_recommendations)

elif system_type == 'Item-Based':
    selected_restaurant_for_rec = st.selectbox("Select a restaurant to get similar recommendations:", user_item_matrix.columns)

    if st.button("Recommend Similar Restaurants", key='item_rec_button'):
        similar_restaurants = get_similar_restaurants(selected_restaurant_for_rec)
        st.write(f"Top restaurants similar to {selected_restaurant_for_rec}:")
        st.write(similar_restaurants)
