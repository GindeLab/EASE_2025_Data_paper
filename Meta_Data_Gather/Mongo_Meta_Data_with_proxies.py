import requests
import time
from pymongo import MongoClient
import json

# List of proxies (Replace these with your own working proxies)
proxies_list = [
    'proxy1_ip:port',
    'proxy2_ip:port',
    'proxy3_ip:port',
    # Add more proxies as needed
]

# Proxy Manager to handle proxy rotation
class ProxyManager:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list
        self.current_proxy_index = 0
        self.last_proxy_change_time = time.time()

    def get_proxy(self):
        now = time.time()
        if now - self.last_proxy_change_time >= 10:
            self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_list)
            self.last_proxy_change_time = now
        return self.proxy_list[self.current_proxy_index]

    def force_change_proxy(self):
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_list)
        self.last_proxy_change_time = time.time()

# Initialize the ProxyManager with your proxies
proxy_manager = ProxyManager(proxies_list)

def make_request_with_proxy(url, retries=3):
    for attempt in range(retries):
        current_proxy = proxy_manager.get_proxy()
        proxies = {
            'http': 'http://' + current_proxy,
            'https': 'https://' + current_proxy,
        }
        try:
            response = requests.get(url, proxies=proxies, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error on attempt {attempt+1} with proxy {current_proxy}: {e}")
            # Force change the proxy
            proxy_manager.force_change_proxy()
            if attempt == retries - 1:
                print(f"All retries failed for URL {url}")
                return None
            else:
                time.sleep(1)  # Wait before retrying

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
    response = make_request_with_proxy(url)
    if response is None:
        print(f"Failed to fetch bug details for Bug ID {bug_id}")
        return None
    try:
        response_json = response.json()
    except json.JSONDecodeError as e:
        print(f"JSON decode error for Bug ID {bug_id}: {e}")
        return None
    if 'bugs' in response_json and response_json['bugs']:
        return response_json['bugs'][0]
    else:
        print(f"No data found or 'bugs' key missing for Bug ID {bug_id}")
        return None

@rate_limited(120)
def get_bug_comments(bug_id):
    url = f'https://bugzilla.mozilla.org/rest/bug/{bug_id}/comment'
    response = make_request_with_proxy(url)
    if response is None:
        print(f"Failed to fetch comments for Bug ID {bug_id}")
        return []
    try:
        response_json = response.json()
    except json.JSONDecodeError as e:
        print(f"JSON decode error for comments of Bug ID {bug_id}: {e}")
        return []
    if 'bugs' in response_json and str(bug_id) in response_json['bugs']:
        comments = response_json['bugs'][str(bug_id)]['comments']
        for i, comment in enumerate(comments):
            comment['Bug report'] = True if i == 0 else False
        return comments
    else:
        print(f"No comments found or 'bugs' key missing for Bug ID {bug_id}")
        return []

@rate_limited(120)
def fetch_author_id(email):
    url = f'https://bugzilla.mozilla.org/rest/user/{email}'
    response = make_request_with_proxy(url)
    if response is None:
        print(f"Failed to fetch author ID for email {email}")
        return None
    try:
        user_data = response.json()
    except json.JSONDecodeError as e:
        print(f"JSON decode error for author ID of email {email}: {e}")
        return None
    if 'users' in user_data and user_data['users']:
        return user_data['users'][0].get('id')
    else:
        print(f"No user data found for email {email}")
        return None

def connect_to_mongo():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["MSR"]
        return db["Bug_meta_data"], db["All_comments"]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None, None

def main():
    start_bug_id = 1884918
    end_bug_id = 1801508
    step = -1
    bug_data_collection, comments_collection = connect_to_mongo()

    if bug_data_collection is None or comments_collection is None:
        print("Database connection could not be established.")
        return
    else:
        print("Database connected successfully.")

    total_bugs = start_bug_id - end_bug_id
    print(f"Total number of bugs to process: {total_bugs}")

    for bug_id in range(start_bug_id, end_bug_id, step):
        print(f"Processing Bug ID: {bug_id}")
        bug_data = get_bug_details(bug_id)
        contributor_emails = set()
        contributor_ids = set()

        if bug_data:
            comments = get_bug_comments(bug_id)
            if comments:
                for comment in comments:
                    email = comment['creator']
                    contributor_emails.add(email)
                    author_id = fetch_author_id(email)
                    if author_id is not None:
                        contributor_ids.add(author_id)
                        comment['author_id'] = author_id
            try:
                if comments:
                    comments_collection.insert_many(comments)
                    print(f"Comments inserted for Bug ID: {bug_id}")
                bug_data['Contributor_email'] = list(contributor_emails)
                bug_data['Contributor_Id'] = list(contributor_ids)
                print(f"Contributor_Id for email {contributor_ids}")

                bug_data_collection.insert_one(bug_data)
                print(f"Bug data inserted for Bug ID: {bug_id}")
            except Exception as e:
                print(f"Failed to insert data for Bug ID {bug_id}: {e}")
        else:
            print(f"No data found for Bug ID: {bug_id}")

    print("Data has been saved to MongoDB.")

if __name__ == "__main__":
    main()
