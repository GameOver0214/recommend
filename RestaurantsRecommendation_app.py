import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline

# Step 1: Load and Preprocess the Dataset
@st.cache_data
def load_data():
    data = pd.read_csv(r'C:\Users\yeder\Desktop\Assignment\Malaysia Restaurant Review Datasets\data_cleaned\GoogleReview_data_cleaned.csv')
    # Preprocessing: Filter out rows with missing values
    data = data[['Restaurant', 'Review', 'Location']].dropna()  # Assuming 'Location' column exists
    return data

data = load_data()

# Step 2: Create a Dummy Price Range (based on keywords in review text)
def infer_price_range(review):
    review = review.lower()
    if any(word in review for word in ['cheap', 'affordable', 'budget', 'inexpensive', 'cut-price', 'low', 'low-priced']):
        return '$'
    elif any(word in review for word in ['moderate', 'reasonable', 'decent']):
        return '$$'
    elif any(word in review for word in ['expensive', 'luxury', 'high-end', 'pricey']):
        return '$$$'
    else:
        return '$$'

data['price_range'] = data['Review'].apply(infer_price_range)

# Step 3: Split the dataset into training and testing data
X = data['Review']
y = data['price_range']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Feature Extraction using TF-IDF and Model Training
model = make_pipeline(
    TfidfVectorizer(stop_words='english'),
    RandomForestClassifier(n_estimators=100, random_state=42)
)

model.fit(X_train, y_train)

# Streamlit Title
st.title("Restaurant Recommender Based on Price Range and Location")

# Step 5: Model Evaluation (Optional)
accuracy = model.score(X_test, y_test)
st.write(f'Model accuracy: {accuracy:.2f}')

# Step 6: Recommend Restaurants Based on User's Price Range and Location
def recommend_restaurants(predicted_price, location, data):
    # Filter the dataset to recommend restaurants with the predicted price range and matching location
    recommendations = data[(data['price_range'] == predicted_price) & (data['Location'].str.contains(location, case=False))]
    # Remove duplicates based on the 'Restaurant' column
    recommendations = recommendations.drop_duplicates(subset='Restaurant')
    # Return the top 5 recommendations
    return recommendations[['Restaurant', 'Review', 'price_range', 'Location']].head(5)

# User Input: Price Range and Location
st.subheader("Find Restaurants by Price Range and Location")
user_price_range = st.selectbox("Select the price range:", ['$', '$$', '$$$'])
user_location = st.text_input("Enter the location you are interested in:")

# Recommend Restaurants
if st.button('Recommend Restaurants'):
    if user_location:
        recommended_restaurants = recommend_restaurants(user_price_range, user_location, data)
        if not recommended_restaurants.empty:
            st.write("\nRecommended Restaurants:")
            st.dataframe(recommended_restaurants)
        else:
            st.write(f"No restaurants found for {user_price_range} in {user_location}.")
    else:
        st.write("Please enter a location.")
