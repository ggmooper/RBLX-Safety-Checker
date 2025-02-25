# RBLX-Safety-Checker
checks for pedophilia in roblox accounts

# How to use:
1. Install python.
2. Run safetyChecker.py
3. Enter a suspicious username
4. see the results in scan_results.txt
5. report them!

# 1️⃣ Steps the Script Follows
**Step 1: Get the User's ID**

You enter a Roblox username when prompted.
The script calls the Roblox API to find the user ID that matches the username.
If the user doesn't exist, the script stops and logs an error.

**Step 2: Fetch Their Friends**

If the user exists, the script requests their friend list from Roblox.
It extracts the user IDs of their friends.
If they have no friends, the script stops and logs a message.

**Step 3: Check for Matches**

The script reads two flagged accounts files:
404accounts.txt → Contains a list of confirmed ERP/predatory accounts.
friends.txt → Contains a list of friends of those accounts (possibly suspicious).
It checks if any of the user's friends are in these lists.

**Step 4: Save Results**
If any friends match the flagged IDs, the script:
Prints their Roblox profile links in the terminal.
Saves the results to scan_results.txt, including the date and time.
If no matches are found, it logs "No suspicious accounts found."

**thanks to ruben sim for making this possible**

# contact me
**discord:** mooper__
