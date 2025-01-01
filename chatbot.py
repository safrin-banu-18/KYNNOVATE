from event_recommendations import process_query, recommend_events, get_feedback, log_interaction
import pandas as pd

# Load the event dataset (CSV)
events_df = pd.read_csv('events.csv')

def chatbot():
    """
    Main chatbot function.
    """
    print("Hello! I'm your Event Discovery Bot. Type 'bye' to end the conversation.")
    
    while True:
        query = input("You: ")
        
        if query.lower() == 'bye':
            print("Chatbot: Goodbye! Take care.")
            break
        
        interests, location = process_query(query)
        response = recommend_events(interests, location, events_df)
        print(f"Chatbot: Here are some recommendations:\n{response}")
        
        feedback = get_feedback()
        log_interaction(query, feedback)

# Start the chatbot
if __name__ == "__main__":
    chatbot()
