class Server:
    def __init__(self):
        self.conversation = []
        
    def process_text(self, text: str) -> dict:
        self.conversation.append(text)
        
        intent = self.get_intent(text)
        
        response = intent
        promptUserAgain = False
        
        return {
            "text": response,
            "promptUserAgain": promptUserAgain
        }
        
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
        
    # check database status
    def merge_pull_requests(self, repo: str) -> str:
        return "Merging pull requests for " + repo

    # run tests

    # read slack

    # rebuild project

    # manage pull requests  