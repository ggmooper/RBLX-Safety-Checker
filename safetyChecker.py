import requests
import re
import json
import os
from datetime import datetime

# File to save scan results
RESULTS_FILE = "scan_results.txt"

def log_result(message):
    """Logs messages to both the console and a file."""
    with open(RESULTS_FILE, "a", encoding="utf-8") as file:
        file.write(f"{datetime.now()} - {message}\n")
    print(message)  # Also print to console for real-time feedback

def get_user_id(username):
    """Fetch the Roblox user ID for a given username using the current API."""
    url = "https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": [username], "excludeBannedUsers": False}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"  # Mimic a real browser
    }
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            user_id = data['data'][0]['id']
            log_result(f"✅ Found User ID: {user_id} for username: {username}")
            return user_id
        else:
            log_result("❌ No data returned for username.")
    else:
        log_result(f"❌ API Error: {response.status_code} - {response.text}")
    
    return None

def get_friends(user_id):
    """Fetch the friends list of a Roblox user by user ID using the current API."""
    url = f"https://friends.roblox.com/v1/users/{user_id}/friends"
    headers = {
        "User-Agent": "Mozilla/5.0"  # Mimic a real browser
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        friends_list = [friend['id'] for friend in data.get('data', [])]
        log_result(f"✅ Found {len(friends_list)} friends for user ID: {user_id}")
        return friends_list
    else:
        log_result(f"❌ Error fetching friends: {response.status_code} - {response.text}")
        return []

def extract_user_ids(file_path):
    """Extract user IDs from URLs in the given file."""
    ids = set()
    if not os.path.exists(file_path):
        log_result(f"⚠️ Warning: {file_path} not found! Skipping...")
        return ids  # Return empty set if file doesn't exist

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.search(r'users/(\d+)', line)
            if match:
                ids.add(match.group(1))

    log_result(f"✅ Extracted {len(ids)} user IDs from {file_path}")
    return ids

def check_for_matches(username):
    log_result(f"\n🔍 Checking for matches for username: {username}")
    user_id = get_user_id(username)
    
    if user_id is None:
        log_result("❌ Username not found. Exiting...")
        return

    log_result(f"🔎 Checking friends for user: {username} (ID: {user_id})")
    
    friends = get_friends(user_id)
    
    if not friends:
        log_result("ℹ️ No friends found for this user.")
        return

    # Use absolute paths for the files
    base_directory = os.path.dirname(os.path.abspath(__file__))
    unsafe_profiles_file = os.path.join(base_directory, '404accounts.txt')
    unsafe_friends_file = os.path.join(base_directory, 'friends.txt')

    unsafe_profiles_ids = extract_user_ids(unsafe_profiles_file)
    unsafe_friends_ids = extract_user_ids(unsafe_friends_file)

    log_result(f"🔄 Checking {len(friends)} friends for matches...")

    # Check for matches
    profile_matches = [f"https://www.roblox.com/users/{friend_id}/profile" for friend_id in friends if str(friend_id) in unsafe_profiles_ids]
    friend_matches = [f"https://www.roblox.com/users/{friend_id}/profile" for friend_id in friends if str(friend_id) in unsafe_friends_ids]

    if profile_matches:
        log_result("\n🚨 Known ERP account(s) found in friends:")
        for match in profile_matches:
            log_result(match)
    
    if friend_matches:
        log_result("\n⚠️ Friends of known ERP account(s) found in friends:")
        for match in friend_matches:
            log_result(match)

    if not profile_matches and not friend_matches:
        log_result("\n✅ No suspicious accounts found.")

if __name__ == "__main__":
    username = input("Enter a Roblox username: ")
    check_for_matches(username)
