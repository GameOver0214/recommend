import streamlit as st
import pandas as pd

# Set the background image using CSS
image_url = "https://cdn.vox-cdn.com/uploads/chorus_image/image/73039055/Valle_KimberlyMotos__1_of_47__websize__1_.0.jpg"
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{image_url}");
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 style="font-size:35px;">Most Popular Restaurants Based on Reviews and Ratings</h1>', unsafe_allow_html=True)

place = st.selectbox("Select the state location:", 
                     ['KL', 'Ipoh', 'JB', 'Kuching', 'Langkawi', 'Melaka', 'Miri', 'Penang', 'Petaling Jaya', 'Shah Alam'])

google_review_data = pd.read_csv('GoogleReview_data_cleaned.csv')
tripadvisor_data = pd.read_csv('TripAdvisor_data_cleaned.csv')

google_review_data.dropna(axis=0, how='any', inplace=True)
tripadvisor_data.dropna(axis=0, how='any', inplace=True)
google_review_data.drop_duplicates(inplace=True, keep=False)
tripadvisor_data.drop_duplicates(inplace=True, keep=False)

if 'Number of Reviews' not in google_review_data.columns:
    google_review_data['Number of Reviews'] = google_review_data['Review'].apply(lambda x: len(x.split()))  # Example assumption
if 'Number of Reviews' not in tripadvisor_data.columns:
    tripadvisor_data['Number of Reviews'] = tripadvisor_data['Review'].apply(lambda x: len(x.split()))  # Example assumption

combined_data = pd.merge(google_review_data, tripadvisor_data, on=['Restaurant', 'Location'], how='inner')
combined_data = combined_data.drop_duplicates(subset=['Restaurant'], keep='first')

combined_data['Combined Rating'] = (combined_data['Rating_x'] + combined_data['Rating_y']) / 2
combined_data['Total Reviews'] = combined_data['Number of Reviews_x'] + combined_data['Number of Reviews_y']

place_df = combined_data[combined_data['Location'].str.lower().str.contains(place.lower())]
sorted_data = place_df.sort_values(by=['Total Reviews', 'Combined Rating'], ascending=[False, False])
sorted_data.reset_index(drop=True, inplace=True)

# Dictionary to map restaurant names to food types
food_type_mapping = {
    'Cafe': ['cafe', 'coffee'],
    'KFC': ['kfc', 'fried chicken', 'fast food'],
    'Pizza Hut': ['pizza', 'pasta'],
    'Chinese Restaurant': ['chinese', 'dimsum', 'wok'],
    'Western Food': ['western', 'grill', 'steak'],
    # Add more mappings as needed
}

# Function to get food type based on restaurant name
def get_food_type(restaurant_name):
    for food_type, keywords in food_type_mapping.items():
        if any(keyword.lower() in restaurant_name.lower() for keyword in keywords):
            return food_type
    return 'Other'

# Get popular restaurants
popular_restaurants = sorted_data[['Restaurant', 'Location', 'Total Reviews', 'Combined Rating']].head(10)

# Assign food types
popular_restaurants['Food Type'] = popular_restaurants['Restaurant'].apply(get_food_type)

popular_restaurants = popular_restaurants.rename(columns={
    'Restaurant': 'Name',
    'Total Reviews': 'Number of Reviews',
    'Combined Rating': 'Average Rating'
})

st.dataframe(popular_restaurants.style.format({
    'Number of Reviews': '{:.0f}',
    'Average Rating': '{:.1f}'
}))
