import requests
import time
import re
import html

def extract_tweet_id(tweet_url):
    match = re.search(r"status/(\d+)", tweet_url)
    return match.group(1) if match else None

def get_tweet_author_id(tweet_id, headers):
    url = f"https://api.twitter.com/2/tweets/{tweet_id}?expansions=author_id"
    res = requests.get(url, headers=headers).json()
    return res['data']['author_id']

def get_liking_users(tweet_id, headers):
    url = f"https://api.twitter.com/2/tweets/{tweet_id}/liking_users"
    res = requests.get(url, headers=headers).json()
    return list(set(u['username'] for u in res.get("data", [])))

def get_retweeters(tweet_id, headers):
    url = f"https://api.twitter.com/2/tweets/{tweet_id}/retweeted_by"
    res = requests.get(url, headers=headers).json()
    return list(set(u['username'] for u in res.get("data", [])))

def get_repliers(tweet_id, headers):
    url = f"https://api.twitter.com/2/tweets/search/recent?query=conversation_id:{tweet_id}&max_results=100"
    res = requests.get(url, headers=headers).json()
    author_ids = list(set(d["author_id"] for d in res.get("data", [])))
    usernames = []
    for uid in author_ids:
        r = requests.get(f"https://api.twitter.com/2/users/{uid}", headers=headers).json()
        if "data" in r:
            usernames.append(r["data"]["username"])
    return list(set(usernames))

def check_follows(usernames, author_id, headers):
    results = {}
    for username in usernames:
        user_res = requests.get(f"https://api.twitter.com/2/users/by/username/{username}", headers=headers).json()
        user_id = user_res.get("data", {}).get("id")
        if not user_id:
            continue
        follow_res = requests.get(f"https://api.twitter.com/2/users/{user_id}/following", headers=headers).json()
        following = follow_res.get("data", [])
        follows = any(u["id"] == author_id for u in following)
        results[username] = follows
    return results

def generate_html(results):
    with open("draw.html", "w", encoding="utf-8") as f:
        f.write("<html><head><style>")
        f.write("table{border-collapse:collapse;}td,th{border:1px solid #000;padding:5px;}")
        f.write("body{font-family:Arial;}</style></head><body>")
        f.write("<h2>User Engagement Grid</h2>")
        f.write("<table><tr><th>Username</th><th>Liked</th><th>Retweeted</th><th>Replied</th><th>Followed</th></tr>")
        for user, actions in results.items():
            f.write(f"<tr><td>{html.escape(user)}</td>")
            for field in ["liked", "retweeted", "replied", "followed"]:
                f.write(f"<td>{'✔' if actions.get(field) else '✘'}</td>")
            f.write("</tr>")
        f.write("</table></body></html>")

def main():
    tweet_url = input("Enter the tweet URL to monitor: ").strip()
    bearer_token = input("Enter your Twitter/X API Bearer Token: ").strip()
    headers = {"Authorization": f"Bearer {bearer_token}"}

    tweet_id = extract_tweet_id(tweet_url)
    if not tweet_id:
        print("Invalid tweet URL.")
        return

    try:
        author_id = get_tweet_author_id(tweet_id, headers)
        print(f"Monitoring tweet ID {tweet_id} from author ID {author_id}...")
    except Exception as e:
        print("Error fetching tweet info:", e)
        return

    while True:
        try:
            print("\nRefreshing engagement data...")
            likes = get_liking_users(tweet_id, headers)
            retweets = get_retweeters(tweet_id, headers)
            replies = get_repliers(tweet_id, headers)

            all_users = set(likes + retweets + replies)

            results = {}
            for user in all_users:
                results[user] = {
                    "liked": user in likes,
                    "retweeted": user in retweets,
                    "replied": user in replies,
                    "followed": False
                }

            follow_checks = check_follows(list(all_users), author_id, headers)
            for user in follow_checks:
                if user in results:
                    results[user]["followed"] = follow_checks[user]

            generate_html(results)
            print(f"Updated draw.html with {len(results)} users. Waiting 300 seconds...\n")
        except Exception as e:
            print("Error during refresh:", e)

        time.sleep(300)

if __name__ == "__main__":
    main()
