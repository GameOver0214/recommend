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

st.markdown('<h1 style="font-size:35px;">Most Popular Restaurants Based on Reviews, Ratings, and Price Range</h1>', unsafe_allow_html=True)

# User input: State location
place = st.selectbox("Select the state location:", 
                     ['KL', 'Ipoh', 'JB', 'Kuching', 'Langkawi', 'Melaka', 'Miri', 'Penang', 'Petaling Jaya', 'Shah Alam'])

# User input: Price range
price = st.selectbox("Select the Price Range ($, $$, $$$):", 
                     ['$', '$$', '$$$'])

# Load the datasets
google_review_data = pd.read_csv('GoogleReview_data_cleaned.csv')
tripadvisor_data = pd.read_csv('TripAdvisor_data_cleaned.csv')

# Data cleaning
google_review_data.dropna(axis=0, how='any', inplace=True)
tripadvisor_data.dropna(axis=0, how='any', inplace=True)
google_review_data.drop_duplicates(inplace=True, keep=False)
tripadvisor_data.drop_duplicates(inplace=True, keep=False)

# Ensure number of reviews columns exist
if 'Number of Reviews' not in google_review_data.columns:
    google_review_data['Number of Reviews'] = google_review_data['Review'].apply(lambda x: len(x.split()))  # Example assumption
if 'Number of Reviews' not in tripadvisor_data.columns:
    tripadvisor_data['Number of Reviews'] = tripadvisor_data['Review'].apply(lambda x: len(x.split()))  # Example assumption

# Combine the two datasets based on Restaurant and Location
combined_data = pd.merge(google_review_data, tripadvisor_data, on=['Restaurant', 'Location'], how='inner')

# Remove duplicates based on Restaurant
combined_data = combined_data.drop_duplicates(subset=['Restaurant'], keep='first')

# Calculate combined rating and total number of reviews
combined_data['Combined Rating'] = (combined_data['Rating_x'] + combined_data['Rating_y']) / 2
combined_data['Total Reviews'] = combined_data['Number of Reviews_x'] + combined_data['Number of Reviews_y']

# Function to determine price range based on review content
def infer_price_range(review):
    review = review.lower()
    if any(word in review for word in [
        'cheap', 'affordable', 'budget', 'inexpensive', 'bargain',
        'low-priced', 'discount', 'sale', 'economical', 'reasonable price',
        'great value', 'good deal', 'worth the price', 'discounted',
        'cost-effective', 'pocket-friendly', 'bank-friendly', 'cost-efficient',
        'thrifty', 'frugal', 'value meal', 'combo deal', 'budget menu', 'special offer'
    ]):
        return '$'
    elif any(word in review for word in [
        'moderate', 'reasonable', 'decent', 'fair price', 'worth it',
        'average price', 'acceptable price', 'fairly priced', 'just right',
        'good quality for the price', 'satisfactory', 'not bad', 'adequate',
        'neither cheap nor expensive', 'affordable luxury', 'value for money',
        'good enough', 'sensible pricing', 'competitively priced', 'comparable',
        'similar to others', 'standard', 'normal price', 'middle of the road'
    ]):
        return '$$'
    elif any(word in review for word in [
        'expensive', 'luxury', 'high-end', 'pricey', 'overpriced',
        'not worth the price', 'top-notch', 'premium', 'elite', 'exclusive',
        'high-quality', 'five-star', 'fine dining', 'gourmet', 'first-class',
        'extravagant', 'lavish', 'extravagant prices', 'steep price',
        'high cost', 'costly', 'heavy on the wallet', 'beyond budget',
        'too much', 'more than expected', 'not affordable', 'highly priced',
        'worth the splurge'
    ]):
        return '$$$'
    else:
        return 'Unknown'  # For reviews that do not match any category

# Apply the price range function to both review columns
combined_data['price_range_x'] = combined_data['Review_x'].apply(infer_price_range)
combined_data['price_range_y'] = combined_data['Review_y'].apply(infer_price_range)

# Assign the price range based on the reviews
combined_data['price_range'] = combined_data[['price_range_x', 'price_range_y']].mode(axis=1)[0]  # Most common price range

# Filter based on location
place_df = combined_data[combined_data['Location'].str.lower().str.contains(place.lower())]

# Filter based on price range
place_df = place_df[place_df['price_range'] == price]

# Sort by total reviews and rating
sorted_data = place_df.sort_values(by=['Total Reviews', 'Combined Rating'], ascending=[False, False])

# Reset index and prepare final dataframe for display
sorted_data.reset_index(drop=True, inplace=True)
popular_restaurants = sorted_data[['Restaurant', 'Location', 'Total Reviews', 'Combined Rating', 'price_range']].head(10)

# Rename columns for display
popular_restaurants = popular_restaurants.rename(columns={
    'Restaurant': 'Name',
    'Total Reviews': 'Number of Reviews',
    'Combined Rating': 'Average Rating',
    'price_range': 'Price Range'
})

# Display the dataframe in Streamlit
st.dataframe(popular_restaurants.style.format({
    'Number of Reviews': '{:.0f}',
    'Average Rating': '{:.1f}'
}))

# Message if no results found
if popular_restaurants.empty:
    st.write(f"No restaurants found for {place} with price range {price}.")
