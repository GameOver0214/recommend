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
    'Chinese Restaurant': ['dim sum', 'noodles', 'stir fry'],
    'Indian Restaurant': ['curry', 'biryani', 'naan'],
    'Mexican Restaurant': ['tacos', 'enchiladas', 'salsa'],
    'Japanese Restaurant': ['sushi', 'ramen', 'tempura'],
    'Thai Restaurant': ['pad thai', 'green curry', 'spring rolls'],
    'Vietnamese Restaurant': ['pho', 'banh mi', 'spring rolls'],
    'Mediterranean Restaurant': ['hummus', 'falafel', 'kebabs'],
    'Korean Restaurant': ['bulgogi', 'kimchi', 'bibimbap'],
    'Middle Eastern Restaurant': ['shawarma', 'tabbouleh', 'mezze'],
    'African Restaurant': ['jollof rice', 'injera', 'bunny chow'],
    'Caribbean Restaurant': ['jerk chicken', 'rice and peas', 'plantains'],
    'Cajun Restaurant': ['gumbo', 'jambalaya', 'po’ boy'],
    'Filipino Restaurant': ['adobo', 'sinigang', 'leche flan'],
    'Pakistani Restaurant': ['biryani', 'karahi', 'nihari'],
    'Sri Lankan Restaurant': ['hoppers', 'kottu', 'string hoppers'],
    'Brazilian Restaurant': ['feijoada', 'picanha', 'coxinha'],
    'Argentinian Restaurant': ['asado', 'empanadas', 'milanesa'],
    'Fusion Cuisine': ['global dishes', 'eclectic flavors', 'creative'],
    'Tapas Bar': ['small plates', 'Spanish', 'sharing'],
    'Street Food': ['food trucks', 'local snacks', 'casual'],
    'Biryani House': ['spiced rice', 'Indian', 'hearty'],
    'Dim Sum House': ['steamed buns', 'dumplings', 'tea'],
    'Sushi Bar': ['sashimi', 'nigiri', 'maki rolls'],
    'Ramen Shop': ['broth', 'noodles', 'Japanese'],
    'Pasta Place': ['lasagna', 'gnocchi', 'risotto'],
    'Noodle Shop': ['pho', 'ramen', 'udon'],
    'Grocery Store': ['fresh produce', 'international', 'variety'],
    'Fish Market': ['fresh seafood', 'sustainable', 'local'],
    'Dessert Shop': ['cakes', 'pastries', 'sweets'],
    'Smoothie Bar': ['smoothies', 'acai bowls', 'healthy drinks'],
    'Cafe': ['coffee', 'pastries', 'light meals'],
    'Ice Cream Parlor': ['ice cream', 'sorbets', 'frozen desserts'],
    'Bakery': ['bread', 'pastries', 'sweets'],
    'Tea House': ['tea', 'snacks', 'light meals'],
    'Snack Bar': ['quick bites', 'light snacks', 'casual'],
    'Vegan Restaurant': ['plant-based', 'healthy', 'creative dishes'],
    'Poke Bowl Shop': ['Hawaiian', 'sushi', 'fresh ingredients'],
    'Curry House': ['curry', 'naan', 'rice dishes'],
    'Souvlaki Grill': ['Greek', 'kebabs', 'pita'],
    'Kebab House': ['grilled meat', 'Middle Eastern', 'wraps'],
    'Hibachi Grill': ['Japanese', 'grilled', 'show cooking'],
    'Biryani Place': ['rice dishes', 'spices', 'Indian'],
    'Samosa Shop': ['Indian', 'snacks', 'fried pastries'],
    'Chaat House': ['snacks', 'Indian', 'street food'],
    'Bento Box Shop': ['Japanese', 'variety', 'healthy'],
    'Falafel Joint': ['Middle Eastern', 'vegetarian', 'snacks'],
    'Gnocchi House': ['Italian', 'pasta', 'comfort food'],
    'Pasta Bar': ['Italian', 'custom pasta', 'variety'],
    'Szechuan Restaurant': ['spicy', 'Chinese', 'numbing'],
    'Buffet': ['variety', 'all-you-can-eat', 'international'],
    'Cantonese Restaurant': ['Chinese', 'dim sum', 'seafood'],
    'Peruvian Restaurant': ['ceviche', 'lomo saltado', 'andean'],
    'Greek Tavern': ['meze', 'grilled meats', 'salads'],
    'Dim Sum Cafe': ['Chinese', 'steamed dishes', 'tea'],
    'Pudding Shop': ['desserts', 'sweet treats', 'creamy'],
    'Tandoori Restaurant': ['Indian', 'grilled', 'spicy'],
    'Buns and Bao House': ['Chinese', 'steamed buns', 'snacks'],
    'Sweet Shop': ['candies', 'desserts', 'sweets'],
    'Crepe Cafe': ['French', 'savory', 'sweet'],
    'Taco Truck': ['Mexican', 'quick bites', 'street food'],
    'Goulash Place': ['Hungarian', 'hearty', 'stew'],
    'Tempura House': ['Japanese', 'fried', 'light'],
    'Nasi Lemak Shop': ['Malaysian', 'rice', 'spicy'],
    'Chili House': ['spicy', 'hearty', 'casual'],
    'Baba Ganoush Cafe': ['Middle Eastern', 'dips', 'vegan'],
    'Fried Rice Restaurant': ['Chinese', 'comfort food', 'fried'],
    'Tapioca Bar': ['bubble tea', 'desserts', 'snacks'],
    'Stroopwafel Shop': ['Dutch', 'sweet', 'snacks'],
    'Sushi Train': ['Japanese', 'conveyor belt', 'sushi'],
    'Rice Bowl Shop': ['Asian', 'rice', 'toppings'],
    'Udon Noodle Shop': ['Japanese', 'noodles', 'soup'],
    'Jamaican Restaurant': ['jerk chicken', 'rice and peas', 'tropical'],
    'Dim Sum Diner': ['Chinese', 'steamed dumplings', 'snacks'],
    'Katsu House': ['Japanese', 'fried', 'pork'],
    'Sushi & Sake Bar': ['Japanese', 'drinks', 'sushi'],
    'Gado Gado Stand': ['Indonesian', 'salad', 'peanut sauce']
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
