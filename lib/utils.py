import re
import json
import os
from typing import List

def save_to_json(formatted_tweets: List[dict], filename: str) -> None:
    """
    Save formatted tweets to Json file in the 'data' folder.
    
    Args:
        formatted_tweets (list): List of dictionaries containing formatted tweets.
        filename (str) : Name of the JSON file to be saved.
    """
    try:
        filename = re.sub(r'[^\w\s.-]', '_', filename)
        data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
        file_path = os.path.join(data_folder, filename)
        
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
            
        tweets_dict = {
            "data" : formatted_tweets
        }
        
        with open(file_path, 'w') as f:
            json.dump(tweets_dict, f, indent=4)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving data to JSON file: {e}")
