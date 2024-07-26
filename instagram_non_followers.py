'''
nano ~/.bashrc
source ~/.bashrc
echo $INSTAGRAM_PASSWORD
python3 instagram_non_followers.py
'''

import instaloader
import os
import time

# Load Instagram credentials from environment variables
username = os.getenv('INSTAGRAM_USERNAME')
password = os.getenv('INSTAGRAM_PASSWORD')

# Ensure credentials are available
if not username or not password:
    print("Please set the INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD environment variables.")
    exit(1)

# Create an instance of Instaloader
L = instaloader.Instaloader()

# Login to Instagram with 2FA handling
try:
    L.login(username, password)
except instaloader.exceptions.TwoFactorAuthRequiredException:
    # If 2FA is required, prompt for the 2FA code
    two_factor_code = input("Enter the 2FA code: ")
    L.context.two_factor_login(two_factor_code)
except instaloader.exceptions.BadCredentialsException:
    print("Invalid username or password.")
    exit(1)
except (instaloader.exceptions.ConnectionException, instaloader.exceptions.QueryReturnedNotFoundException) as e:
    print(f"Connection or query error: {e}")
    exit(1)

# Get your profile
profile = instaloader.Profile.from_username(L.context, username)

# Initialize sets for followers and followees
followers = set()
followees = set()

# Fetch followers
print("Fetching followers...")
start_time = time.time()
try:
    for follower in profile.get_followers():
        followers.add(follower.username)
        time.sleep(1)  # Adding a delay to prevent rate limiting
except (instaloader.exceptions.ConnectionException, instaloader.exceptions.QueryReturnedNotFoundException) as e:
    print(f"Error fetching followers: {e}")
    exit(1)
print(f"Time taken to fetch followers: {time.time() - start_time:.2f} seconds")

# Fetch followees
print("Fetching followees...")
start_time = time.time()
try:
    for followee in profile.get_followees():
        followees.add(followee.username)
        time.sleep(1)  # Adding a delay to prevent rate limiting
except (instaloader.exceptions.ConnectionException, instaloader.exceptions.QueryReturnedNotFoundException) as e:
    print(f"Error fetching followees: {e}")
    exit(1)
print(f"Time taken to fetch followees: {time.time() - start_time:.2f} seconds")

# Identify non-followers
non_followers = followees - followers

print("Users who don't follow you back:")
for user in non_followers:
    print(user)
