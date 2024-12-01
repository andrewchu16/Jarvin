from spacy.matcher import Matcher
from dotenv import load_dotenv
import spacy
import os
import random
import requests
load_dotenv()

GITHUB_PAT = os.getenv("GITHUB_PAT")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_WORKFLOW_ID = os.getenv("GITHUB_WORKFLOW_ID")

class Server:
    def __init__(self):
        self.conversation = []
        self.nlp = spacy.load('./backend/custom_ner_model')
        
    def process_text(self, text: str) -> dict:
        self.conversation.append(text)
        
        intent = self.get_intent(text)
        
        entities = self.extract_custom_entities(text)
        
        response, prompt_user_again = self.get_response(intent, entities)        
        
        return {
            "text": response,
            "intent": intent,
            "promptUserAgain": prompt_user_again
        }
        
    def get_response(self, intent, entities):
        response = "I'm sorry, an unknown error occurred. Can you please try again?"
        prompt_user_again = False
        if intent == "get_database_status":
            response = f"The database is serving {random.randrange(10)} reads per minute and {random.randrange(4)} writes per minute."
            
        elif intent == "merge_pr": # works
            response = self.merge_pr(GITHUB_PAT, GITHUB_REPO, GITHUB_OWNER)
            
        elif intent == "read_slack_mentions":
            channel = entities["slack_channel"]
            response = f"I could not find any mentions in the {channel} channel. Please try again."
            
        elif intent == "run_tests": # works
            ref = entities["branch"]
            response = self.run_tests(GITHUB_PAT, GITHUB_REPO,GITHUB_OWNER, GITHUB_WORKFLOW_ID, ref)
            
        elif intent == "rebuild_project": # works
            response = self.run_build(GITHUB_OWNER, GITHUB_REPO, "main", GITHUB_PAT)
            
        elif intent == "unknown_intent":
            response = "I'm sorry, I don't understand. Can you please try again?"
            prompt_user_again = True
            
        return response, prompt_user_again
        
    def get_intent(self, text: str) -> str:
        text = text.strip().lower()
        intents = {
            "status_database": {
                "keywords": ["status", "database"],
                "action": "get_database_status"
            },
            "merge_pull_requests": {
                "keywords": ["merge", "pull request", "prs"],
                "action": "merge_pr"
            },
            "read_slack_mentions": {
                "keywords": ["read", "slack", "mentions"],
                "action": "read_slack_mentions"
            },
            "run_tests": {
                "keywords": ["run", "tests"],
                "action": "run_tests"
            },
            "rebuild_project": {
                "keywords": ["rebuild", "project"],
                "action": "rebuild_project"
            },
        }
        
        for intent_name, details in intents.items():
            if any(keyword in text for keyword in details["keywords"]):
                return details["action"]
        
        return "unknown_intent"
        
    def extract_custom_entities(self, user_input):
        doc = self.nlp(user_input)
        
        entities = {}
        
        for ent in doc.ents:
            entities[ent.label_.lower()] = ent.text

        return entities
    
    def run_tests(self, token, repo, owner, workflow_id, ref):
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        data = {
            "ref": ref
        }

        response = requests.post(
            f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches",
            headers=headers,
            json=data,
        )

        if response.status_code == 204:
            return ("Workflow triggered successfully!")
        else:
            print(response.json())
            return (f"I was unable to run tests. I received error code {response.status_code}")

    def merge_pr(self, token, repo, owner):
        # Step 1: Get the most recent pull request
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }
        params = {
            "state": "open",
            "sort": "updated",
            "direction": "desc"
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200 and response.json():
            most_recent_pr = response.json()[0]  # Get the first PR in the list
            pr_number = most_recent_pr["number"]
            print(f"Most recent PR found: #{pr_number} - {most_recent_pr['title']}")

            # Step 2: Merge the pull request
            merge_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/merge"
            merge_data = {
                "commit_title": f"Merging PR #{pr_number}: {most_recent_pr['title']}",
                "merge_method": "merge"  # Options: merge, squash, rebase
            }
            merge_response = requests.put(merge_url, headers=headers, json=merge_data)

            if merge_response.status_code == 200:
                return ("Pull request merged successfully!")
            else:
                print(merge_response.json())
                return (f"I was unable to merge PR #{pr_number}: {merge_response.status_code}")
        else:
            return ("I could not find any open pull requests.")
    
    def run_build(self, repo_owner, repo_name, branch="main", token=None):
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/workflows/build-branch.yml/dispatches"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }
        payload = {
            "ref": branch
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 204:
            return (f"Right away. I have started the build task on '{branch}'.")
        else:
            print(response.json())
            return (f"Sorry, I was unable to build the project. I received error code {response.status_code}")