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
        'cheap', 'affordable', 'budget', 'inexpensive', 'bargain', 'low-cost',
        'economical', 'good deal', 'low-priced', 'discount', 'sale', 
        'value for money', 'pocket-friendly', 'wallet-friendly', 'frugal', 
        'cost-effective', 'reasonable price', 'budget-friendly', 'inexpensive options',
        'family-friendly prices', 'daily specials', 'budget menu', 'cheap eats',
        'special offer', 'value meal', 'economical choices', 'cheap dining',
        'discount menu', 'affordable options', 'cost-efficient', 'low-end',
        'wallet-friendly choices', 'inexpensive dining', 'great prices', 
        'cheap lunch', 'value snacks', 'wallet-conscious', 'budget dining', 
        'low-cost meal', 'economical meal', 'special pricing', 'affordable eats', 
        'best budget', 'price-friendly', 'unbeatable prices', 'economical eats', 
        'thrifty meal', 'low-budget options', 'budget-friendly eats', 
        'low-price specials', 'student-friendly', 'cheap rates', 'low-cost dining', 
        'great value for money', 'thrifty choices', 'cut-rate', 'wallet-friendly meal', 
        'budget-conscious', 'discounted rates', 'economy-priced', 'discount dining', 
        'affordable rates', 'penny-pinching', 'cost-effective options', 'cheap specials',
        'affordable dining', 'budget options', 'cost-saving', 'low-end meals', 
        'wallet-wise', 'savings deal', 'budget combo', 'pocket-friendly meals', 
        'value-driven', 'cheap treats', 'frugal dining', 'good prices', 
        'economical dining', 'thrifty eats', 'sensible pricing', 'budget bargain', 
        'value for less', 'low-cost deals', 'student specials', 'bargain prices', 
        'discount treats', 'frugal choices', 'budget-friendly prices', 
        'low-cost options', 'smart spending', 'economical finds', 'deal meals', 
        'low-cost specials', 'affordable bites', 'economical bargains', 
        'price-slashing', 'cost-effective meals', 'great cheap eats', 
        'budget-worthy', 'penny-wise'
    ]):
        return '$'  # Cheap
    elif any(word in review for word in [
        'moderate', 'reasonable', 'decent', 'fair price', 'worth it', 
        'good value', 'fairly priced', 'average price', 'just right', 
        'sensible pricing', 'acceptable price', 'average quality', 'solid choice', 
        'good enough', 'reasonable quality', 'typical pricing', 'nice atmosphere', 
        'affordable luxury', 'moderate options', 'quality food', 'value experience', 
        'good balance', 'moderate pricing', 'decent value', 'reasonably priced meals', 
        'quality at a price', 'value-for-quality', 'satisfactory', 'adequate pricing', 
        'fair value', 'decent portions', 'worthwhile', 'worth the price', 
        'solid meal', 'acceptable quality', 'average experience', 'mid-range', 
        'reasonably priced eats', 'fair pricing', 'reasonable expectations', 
        'not too pricey', 'above average', 'everyday pricing', 'moderate quality', 
        'well-priced', 'solid offering', 'sensible value', 'reasonable meal', 
        'decent options', 'quality without splurge', 'fair deal', 'good atmosphere', 
        'okay prices', 'quality service', 'reasonable choices', 'middle of the road', 
        'fair portions', 'pleasant dining', 'worthwhile meal', 'good quality for the price', 
        'reasonable rates', 'standard pricing', 'sufficient value', 'sensible meal prices', 
        'decent quality food', 'moderate expectations', 'not over the top', 
        'balanced experience', 'fair offerings', 'sensible dining', 'cost-justified', 
        'typical costs', 'reliable value', 'satisfactory pricing', 'value-oriented', 
        'reasonable meal prices', 'average dining', 'accessible prices', 
        'moderate flavors', 'pleasant experience', 'decent environment', 
        'fair pricing options', 'balanced offerings', 'practical prices', 
        'acceptable dining', 'fair comparisons', 'reasonable options', 'not too high', 
        'satisfactory quality', 'good value choices', 'solid standards', 
        'sensible prices', 'moderate service', 'everyday quality', 'standard offerings', 
        'acceptable pricing', 'reasonable enjoyment', 'decent flavors', 
        'practical pricing'
    ]):
        return '$$'  # Moderate
    elif any(word in review for word in [
        'expensive', 'luxury', 'high-end', 'pricey', 'overpriced', 
        'extravagant', 'premium', 'elite', 'exclusive', 'lavish', 
        'costly', 'gourmet', 'fine dining', 'first-class', 'five-star', 
        'exquisite', 'top-notch', 'high-quality', 'worth the splurge', 
        'upscale', 'exceptional quality', 'luxurious', 'indulgent', 
        'deluxe', 'prestigious', 'extravagant experience', 'high-cost', 
        'premium pricing', 'cost prohibitive', 'high-class', 'luxury dining', 
        'splurge-worthy', 'extravagant prices', 'fancy', 'lavish dining', 
        'ritzy', 'opulent', 'cost prohibitive', 'exclusive experience', 
        'premium menu', 'high-tier', 'gourmet experience', 'fine cuisine', 
        'upscale offerings', 'luxury experience', 'high-end service', 
        'lavishly priced', 'top-tier dining', 'costly choices', 
        'elite offerings', 'extravagant meals', 'posh', 'extravagant options', 
        'exquisite dining', 'five-star quality', 'elite atmosphere', 
        'luxurious flavors', 'steep prices', 'high-end options', 
        'premium experience', 'overpriced items', 'first-rate', 
        'extraordinary', 'classy', 'high-status', 'high-priced meals', 
        'lavish quality', 'extravagant flavors', 'luxurious presentation', 
        'exceptional service', 'high-ticket', 'premium value', 
        'superior quality', 'upscale choices', 'deluxe experience', 
        'five-star service', 'luxury menu', 'refined', 'elite dining', 
        'exclusive prices'
    ]):
        return '$$$'  # Expensive
    else:
        return 'Unknown'  # Default to moderate if no keywords found

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
