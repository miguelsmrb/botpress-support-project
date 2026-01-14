import requests
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
WEBHOOK = os.getenv("DISCORD_WEBHOOK")
REPO_OWNER = "miguelsmrb" 
REPO_NAME = "botpress-support-project"

def fetch_github_issues():
    url = f"https://api.github.com/repos/miguelsmrb/botpress-support-project/issues"
    headers = {"Authorization": f"token {TOKEN}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch issues. Status:{response.status_code}")
        return []

def support_alert():
    issues = fetch_github_issues()
    keywords = ["bug", "critical", "error", "urgent", "please help!", "asap"]
    
    for issue in issues:
        title = issue['title'].lower()
        if any(word in title for word in keywords):
            print(f"MATCH FOUND: {issue['title']}")
            
            # Format the message for Discord
            payload = {
                "content": f"🚨 **Urgent Issue Alert**\n**Issue:** {issue['title']}\n**Author:** {issue['user']['login']}\n**Link:** {issue['html_url']}"
            }
            requests.post(WEBHOOK, json=payload)
        else:
            print(f"Skipping: {issue['title']} (No keywords match)")

if __name__ == "__main__":
    support_alert()