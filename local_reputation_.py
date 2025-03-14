import requests
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient

# Rate limit decorator
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

# MongoDB connection setup
def connect_to_mongo(collection_name):
    client = MongoClient("mongodb://localhost:27017/")
    # client = MongoClient("mongodb+srv://JaGrIt:jagrit@cluster0.fegfu.mongodb.net/")
    db = client["MSR"]
    return db[collection_name]

# Function to fetch user details
@rate_limited(200)
def fetch_user_details(author_id):
    if not author_id:
        print("Author ID is NaN or invalid, skipping.")
        return None

    url = f'https://bugzilla.mozilla.org/user_profile?user_id={author_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed for user_id {author_id}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        # Extract required details
        user_details = {
            "User ID": author_id,
            "User Name": soup.select_one('div.vcard a').text.strip() if soup.select_one('div.vcard a') else None,
            "Created On": soup.select_one('tr:contains("Created") td:last-of-type').text.strip() if soup.select_one('tr:contains("Created") td:last-of-type') else None,
            "Last Activity": soup.select_one('tr:contains("Last activity") td:last-of-type').text.strip() if soup.select_one('tr:contains("Last activity") td:last-of-type') else None,
            "Permissions": soup.select_one('tr:contains("Permissions") td:last-of-type').text.strip() if soup.select_one('tr:contains("Permissions") td:last-of-type') else None,
            "Bugs Filed": int(soup.select_one('tr:contains("Bugs filed") td.numeric').text.strip()) if soup.select_one('tr:contains("Bugs filed") td.numeric') else 0,
            "Comments Made": int(soup.select_one('tr:contains("Comments made") td.numeric').text.strip()) if soup.select_one('tr:contains("Comments made") td.numeric') else 0,
            "Assigned to": int(soup.select_one('tr:contains("Assigned to") td.numeric').text.strip()) if soup.select_one('tr:contains("Assigned to") td.numeric') else 0,
            "Assigned to and Fixed": int(soup.select_one('tr:contains("Assigned to and fixed") td.numeric').text.strip()) if soup.select_one('tr:contains("Assigned to and fixed") td.numeric') else 0,
            "Commented on": int(soup.select_one('tr:contains("Commented on") td.numeric').text.strip()) if soup.select_one('tr:contains("Commented on") td.numeric') else 0,
            "QA Contact": int(soup.select_one('tr:contains("QA-Contact") td.numeric').text.strip()) if soup.select_one('tr:contains("QA-Contact") td.numeric') else 0,
            "Patches Submitted": int(soup.select_one('tr:contains("Patches submitted") td.numeric').text.strip()) if soup.select_one('tr:contains("Patches submitted") td.numeric') else 0,
            "Patches Reviewed": int(soup.select_one('tr:contains("Patches reviewed") td.numeric').text.strip()) if soup.select_one('tr:contains("Patches reviewed") td.numeric') else 0,
            "Bugs Poked": int(soup.select_one('tr:contains("Bugs poked") td.numeric').text.strip()) if soup.select_one('tr:contains("Bugs poked") td.numeric') else 0
        }
        return user_details
    except Exception as e:
        print(f"Error processing data for user_id {author_id}: {e}")
        return None

# Connect to the MongoDB collections
bug_reports_collection = connect_to_mongo("Bug_meta_data")
reputation_collection = connect_to_mongo("Reporter Reputation")

# Fetch contributor IDs from the bug reports collection
bug_reports = bug_reports_collection.find().sort("_id", -1)

for report in bug_reports:
    contributor_ids = report.get("Contributor_Id", [])
    for author_id in contributor_ids:
        # Check if the user already exists in the reputation collection
        existing_user = reputation_collection.find_one({"User ID": author_id})
        if existing_user:
            print(f"User ID {author_id} already exists in the database. Skipping insertion.")
            continue  # Skip to the next author_id
        user_details = fetch_user_details(author_id)
        if user_details:
            try:
                # Insert user details into the reputation collection
                reputation_collection.insert_one(user_details)
                print(f"Inserted reputation data for Author ID: {author_id}")
            except Exception as e:
                print(f"Error inserting data for user_id {author_id} into MongoDB: {e}")

print("Data processing completed and saved to MongoDB.")
