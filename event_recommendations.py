import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from geopy.geocoders import Nominatim
from datetime import datetime
import os

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Geolocation setup using Geopy
geolocator = Nominatim(user_agent="event_chatbot")

# Predefined categories for event recommendations
categories = ["Music", "Technology", "Fitness", "Art", "Cooking"]

def process_query(query):
    """
    Process user input to extract interests and location.
    """
    # query = query.lower()
    
    # Tokenize the query and remove stopwords
    tokens = word_tokenize(query)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    # Extract potential interests and location (simple method)
    interests = [word for word in filtered_tokens if word in categories]
    location = extract_location(query)
    
    return interests, location

def extract_location(query):
    """
    Extract location from the query using geopy.
    """
    try:
        location = geolocator.geocode(query)
        if location:
            return location.address
    except Exception as e:
        print("Error in location extraction:", e)
    return None

def recommend_events(interests, location, events_df):
    """
    Recommend events based on user interests and location.
    """
    # Start with a copy of the events data
    filtered_df = events_df.copy()
    print("Filtered DataFrame (Initial Copy):")
    print(filtered_df)

    # Initialize empty DataFrames
    result_categories = pd.DataFrame()  # Initialize an empty DataFrame for categories
    result_locations = pd.DataFrame()   # Initialize an empty DataFrame for locations
    result = pd.DataFrame()  # Initialize an empty DataFrame to store results
    print("\nEmpty DataFrames for categories and locations initialized:")
    print(f"Categories: {result_categories.shape}, Locations: {result_locations.shape}")

    # Filter by interests (category)
    if interests:
        result_categories = filtered_df[filtered_df['category'].isin(interests)]
        print("\nFiltered by Interests (Category):")
        print(result_categories)
    
    # Filter by location
    if location:
        result_locations = filtered_df[filtered_df['location'].str.contains(location, case=False, na=False)]
        print("\nFiltered by Location:")
        print(result_locations)

    # Combine both category and location filters using the intersection
    if not result_categories.empty and not result_locations.empty:
        result = pd.merge(result_categories, result_locations, how='inner', on=['event_name', 'category', 'location', 'date', 'description'])
        print("\nMerged DataFrame (Category and Location):")
        print(result)
    elif not result_categories.empty:
        result = result_categories
        print("\nUsing only Category Filter:")
        print(result)
    elif not result_locations.empty:
        result = result_locations
        print("\nUsing only Location Filter:")
        print(result)

    # If no events match, provide a default message
    if result.empty:
        return "Sorry, I couldn't find any events matching your interests and location."
    
    # Return the top 3 recommendations
    recommendations = result.head(3)
    print("\nTop 3 Recommendations:")
    print(recommendations)

    return recommendations[['event_name', 'category', 'location', 'date', 'description']].to_string(index=False)

def get_feedback():
    """
    Get feedback from the user (basic learning mechanism).
    """
    feedback = input("Was this recommendation helpful? (yes/no): ").strip().lower()
    return feedback == 'yes'

def log_interaction(query, feedback):
    """
    Log user interactions and feedback for further analysis or improvements.
    """
    log_data = {'query': query, 'feedback': feedback, 'timestamp': datetime.now()}
    log_df = pd.DataFrame([log_data])
    
    if os.path.exists('interaction_log.csv'):
        log_df.to_csv('interaction_log.csv', mode='a', header=False, index=False)
    else:
        log_df.to_csv('interaction_log.csv', mode='w', header=True, index=False)
