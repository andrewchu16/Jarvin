class Server:
    def __init__(self):
        self.conversation = []
        
    def process_text(self, text: str) -> dict:
        self.conversation.append(text)
        
        response = "Jarvin says hi"
        promptUserAgain = False
        
        return {
            "text": response,
            "promptUserAgain": promptUserAgain
        }
        
    # check database status

    # run tests

    # read slack

    # rebuild project

    # manage pull requests  