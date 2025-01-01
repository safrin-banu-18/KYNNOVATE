from flask import Flask, request, jsonify, render_template
from event_recommendations import process_query, recommend_events
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__, template_folder='templates')

# Load the event dataset
events_df = pd.read_csv('events.csv')

# Interaction log file path
log_file = 'interaction_log.csv'

def log_interaction(query, response):
    """
    Log user interactions in interaction_log.csv.
    """
    log_data = {
        'query': query,
        'response': response,
        'timestamp': datetime.now()
    }
    log_df = pd.DataFrame([log_data])

    if os.path.exists(log_file):
        log_df.to_csv(log_file, mode='a', header=False, index=False)
    else:
        log_df.to_csv(log_file, mode='w', header=True, index=False)

@app.route('/')
def home():
    return render_template('kyn.html')

@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Fetch and return interaction logs.
    """
    if os.path.exists(log_file):
        logs = pd.read_csv(log_file)
        return logs.to_html(index=False)
    else:
        return "No logs found."

@app.route('/chat', methods=['POST'])
def chat():
    user_query = request.json.get('query', '')

    if not user_query:
        return jsonify({"error": "Query not provided"}), 400

    # Process the query
    interests, location = process_query(user_query)
    response = recommend_events(interests, location, events_df)

    # Log the interaction
    log_interaction(user_query, response)

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
