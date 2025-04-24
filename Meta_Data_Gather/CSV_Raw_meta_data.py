import requests
import time
import pandas as pd
from pymongo import MongoClient

def rate_limited(max_per_minute):
    min_interval = 60.0 / float(max_per_minute)
    def decorate(func):
        last_time_called = [0.0]
        def rate_limited_function(*args, **kwargs):
            elapsed = time.time() - last_time_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            last_time_called[0] = time.time()
            return func(*args, **kwargs)
        return rate_limited_function
    return decorate

@rate_limited(120)
def get_bug_details(bug_id):
    url = f'https://bugzilla.mozilla.org/rest/bug/{bug_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Handle HTTP errors
        response_json = response.json()
        if 'bugs' in response_json and response_json['bugs']:
            return response_json['bugs'][0]
        else:
            print(f"No data found or 'bugs' key missing for Bug ID {bug_id}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bug details for Bug ID {bug_id}: {e}")
        return None

def connect_to_mongo():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["EASE"]
        return db["Bug_meta"]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def main():
    # Load bug IDs from Excel file
    try:
        df = pd.read_csv("bugs-2025-02-23.csv")
        bug_ids = df["Bug ID"].dropna().astype(int).tolist()
        # bug_ids = bug_ids[:10]
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    bug_meta_collection = connect_to_mongo()
    if bug_meta_collection is None:
        print("Database connection could not be established.")
        return
    else:
        print("Database connected successfully.")

    total_bugs = len(bug_ids)
    print(f"Total number of bugs to process: {total_bugs}")

    for bug_id in bug_ids:
        print(f"Processing Bug ID: {bug_id}")
        bug_data = get_bug_details(bug_id)
        if bug_data:
            try:
                bug_meta_collection.insert_one(bug_data)
                print(f"Bug data inserted for Bug ID: {bug_id}")
            except Exception as e:
                print(f"Failed to insert data for Bug ID {bug_id}: {e}")
        else:
            print(f"No data found for Bug ID: {bug_id}")

    print("Data has been saved to MongoDB.")

if __name__ == "__main__":
    main()
