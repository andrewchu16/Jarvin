from spacy.matcher import Matcher
from dotenv import load_dotenv
import spacy
import os
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
            response = "The database is serving 6 reads per minute and 2 writes per minute."
        elif intent == "merge_pr": # works
            pass
        elif intent == "read_slack_mentions":
            pass
        elif intent == "run_tests": # works
            ref = entities["branch"]
            response = self.run_tests(GITHUB_PAT, GITHUB_REPO,GITHUB_OWNER, GITHUB_WORKFLOW_ID, ref)
        elif intent == "rebuild_project":
            response = f"I could not find any build tasks on {GITHUB_REPO}. Please try again."
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

        print(f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}")
        response = requests.post(
            f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches",
            headers=headers,
            json=data,
        )

        if response.status_code == 204:
            return ("Workflow triggered successfully!")
        else:
            print(response.json())
            return (f"Failed to trigger workflow: {response.status_code}")
