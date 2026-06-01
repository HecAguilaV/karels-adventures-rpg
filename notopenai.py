class NotOpenAI:
    # Pre-condition - api_key is a string
    # Post-condition - initializes a mock client instance
    def __init__(self, api_key=""):
        self.api_key = api_key
