import streamlit as st
import pandas as pd

# Set the background image using CSS
import streamlit as st
image_url = "https://cdn.vox-cdn.com/uploads/chorus_image/image/73039055/Valle_KimberlyMotos__1_of_47__websize__1_.0.jpg"
# Sample data (you can replace this with your actual data)
restaurants = [
    {"name": "The Gourmet Kitchen", "url": "https://gourmetkitchen.com"},
    {"name": "Sushi World", "url": "https://sushiworld.com"},
    {"name": "Pasta Paradise", "url": "https://pastaparadise.com"},
    {"name": "BBQ Haven", "url": "https://bbqhaven.com"},
]

# Title of the app
st.title("Restaurant Explorer")

# Subtitle
st.subheader("Discover the Best Restaurants Around You")

# Loop through the restaurants and display them
for restaurant in restaurants:
    st.write(f"**{restaurant['name']}**")
    st.write(f"[Visit Website]({restaurant['url']})")
    st.write("---")  # Adds a line break

# Footer
st.write("Powered by Streamlit")


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
    "Savor Bistro": "American",
    "Spice Symphony": "Indian",
    "La Bella Italia": "Italian",
    "Tokyo Sushi House": "Japanese",
    "Café Parisien": "French",
    "Taco Haven": "Mexican",
    "Mediterranean Delights": "Mediterranean",
    "Taste of Thailand": "Thai",
    "Gourmet Burger Bar": "American",
    "Pasta Paradise": "Italian",
    "Curry Corner": "Indian",
    "Dragon Wok": "Chinese",
    "The Greenhouse Café": "Vegetarian",
    "El Mariachi": "Mexican",
    "Savory Crepes": "French",
    "Noodle Nirvana": "Asian Fusion",
    "Smoky BBQ Shack": "Barbecue",
    "Seaside Seafood Grill": "Seafood",
    "Flavors of Ethiopia": "Ethiopian",
    "Chili's Chophouse": "American",
    "Cafe Kawaii": "Japanese",
    "Fresh Catch": "Seafood",
    "Mama Mia's": "Italian",
    "Spice Route": "Indian",
    "The Rustic Table": "American",
    "Bistro Belle": "French",
    "Sushi Sensation": "Japanese",
    "Café Aromas": "Coffee Shop",
    "Zesty Zucchini": "Vegetarian",
    "Mamma's Kitchen": "Italian",
    "Taste of Persia": "Persian",
    "Pita Palace": "Mediterranean",
    "Naan & Curry": "Indian",
    "Dragonfly Bistro": "Asian Fusion",
    "Burgers & Brews": "American",
    "The Spice Rack": "Indian",
    "Ginger Garlic": "Asian Fusion",
    "Pizza Perfection": "Italian",
    "Taco Loco": "Mexican",
    "Rustic Roots": "American",
    "Himalayan Heights": "Nepali",
    "Bistro 77": "French",
    "Seafood Spectacular": "Seafood",
    "Wok & Roll": "Asian Fusion",
    "Grill & Chill": "American",
    "Spicy Thai Kitchen": "Thai",
    "Pastabilities": "Italian",
    "Sizzling BBQ": "Barbecue",
    "The Healthy Bite": "Health Food",
    "Tandoori Nights": "Indian",
    "Baguette & Co.": "French",
    "Urban Sushi": "Japanese",
    "The Curry Leaf": "Indian",
    "Cheesy Crust": "Italian",
    "The Olive Tree": "Mediterranean",
    "Sushi & Sake": "Japanese",
    "Harvest Moon Café": "Vegetarian",
    "Fusion Flavors": "Asian Fusion",
    "Little Italy": "Italian",
    "The Taco Stand": "Mexican",
    "The Seafood Market": "Seafood",
    "Café Italia": "Italian",
    "Taste of the Bay": "Seafood",
    "Kebab House": "Middle Eastern",
    "Savory Bites": "American",
    "The Green Fork": "Vegetarian",
    "Sushi Town": "Japanese",
    "Waffles & More": "Breakfast",
    "The Spice House": "Indian",
    "Little India": "Indian",
    "Spicy Noodle Shop": "Asian Fusion",
    "Beef & Brew": "American",
    "The Mediterranean Plate": "Mediterranean",
    "Nasi Lemak Delight": "Malaysian",
    "Roti Canai Corner": "Malaysian",
    "Satay Station": "Malaysian",
    "Penang Street Eats": "Malaysian",
    "Curry House": "Indian",
    "Mamak Munchies": "Malaysian",
    "Kuala Lumpur Kitchen": "Malaysian",
    "Malaysian Spice": "Malaysian",
    "Hainan Chicken Rice House": "Malaysian",
    "The Laksa Lounge": "Malaysian",
    "Rendang Republic": "Malaysian",
    "Teh Tarik Café": "Malaysian",
    "Bubur Ayam Bistro": "Malaysian",
    "Sambal Shack": "Malaysian",
    "Satey Station": "Malaysian",
    "Kampung Kitchen": "Malaysian",
    "Fried Noodle Haven": "Malaysian",
    "Murtabak Mania": "Malaysian",
    "Char Kway Teow Express": "Malaysian",
    "Nasi Kandar Hub": "Malaysian",
    "Kari Kuali": "Malaysian",
    "Cendol & Co.": "Malaysian",
    "Asam Pedas Palace": "Malaysian",
    "Nasi Briyani Bazaar": "Malaysian",
    "Soto Station": "Malaysian",
    "Malaysian Street Food": "Malaysian",
    "Roti John Joint": "Malaysian",
    "Pandan Flavors": "Malaysian",
    "Sambal Belacan Bistro": "Malaysian",
    "Malaysian Flavors": "Malaysian",
    "Bubur Lambuk House": "Malaysian",
    "Kueh Kueh Delight": "Malaysian",
    "Chili Pan Mee": "Malaysian",
    "Kaya Toast Café": "Malaysian",
    "Tandoori & Nasi": "Indian",
    "Curry Puff Palace": "Indian",
    "Banana Leaf Bistro": "Indian",
    "Mee Goreng Corner": "Malaysian",
    "Sambal Sotong": "Malaysian",
    "Fried Rice Fiesta": "Malaysian",
    "Nasi Campur Café": "Malaysian",
    "Kedai Kopi Tradisional": "Malaysian",
    "Noodle Nest": "Asian Fusion",
    "Coconut Grove": "Tropical",
    "Malaysian Masakan": "Malaysian",
    "Sago & Sugar": "Malaysian",
    "Goreng Pisang Place": "Malaysian",
    "Laksa Lemak": "Malaysian",
    "Teriyaki & Curry": "Japanese",
    "Hokkien Mee House": "Malaysian",
    "Sushi Wave": "Japanese",
    "Chowder House": "Seafood",
    "The Green Plate": "Vegetarian",
    "Indian Harvest": "Indian",
    "Pasta Fresca": "Italian",
    "Taqueria Delight": "Mexican",
    "Soul Food Café": "American",
    "Mochi Munchies": "Japanese",
    "Brunch Bistro": "American",
    "The BBQ Pit": "Barbecue",
    "Bistro de Paris": "French",
    "Fried Chicken Co.": "American",
    "The Burger Spot": "American",
    "Artisan Pizza": "Italian",
    "Gumbo Galore": "Cajun",
    "The Sushi Bar": "Japanese",
    "Pizza and Pasta Place": "Italian",
    "Noodle Nook": "Asian Fusion",
    "Café Verde": "Vegetarian",
    "Seafood Sensation": "Seafood",
    "Mamma's Pizzeria": "Italian",
    "Cafe Express": "American",
    "Curry House": "Indian",
    "Beef Wellington Bistro": "American",
    "Crepe Café": "French",
    "Pho Haven": "Vietnamese",
    "Korean BBQ Grill": "Korean",
    "Café de la Mer": "French",
    "Hibachi Grill": "Japanese",
    "The Pasta Pot": "Italian",
    "Mexican Fiesta": "Mexican",
    "Banh Mi Paradise": "Vietnamese",
    "Bratwurst House": "German",
    "Sushi Express": "Japanese",
    "The Lobster Trap": "Seafood",
    "Aromatic Thai": "Thai",
    "The Spice Merchant": "Indian",
    "The Curry Pot": "Indian",
    "Fusion Sushi": "Japanese",
    "Creole Kitchen": "Cajun",
    "Gnocchi & More": "Italian",
    "The Taco Truck": "Mexican",
    "The Grilled Cheese Bar": "American",
    "Szechuan Spice": "Chinese",
    "The Breakfast Bar": "Breakfast",
    "Sushi Wave": "Japanese",
    "Chowder House": "Seafood",
    "The Green Plate": "Vegetarian",
    "Indian Harvest": "Indian",
    "Pasta Fresca": "Italian",
    "Taqueria Delight": "Mexican",
    "Soul Food Café": "American"
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
