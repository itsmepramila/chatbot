from langchain import LangChain
from openai import OpenAI

# Initialize LangChain
lc = LangChain()

# Initialize OpenAI with your API key
openai.api_key = 'your_openai_api_key'

class Chatbot:
    def __init__(self):
        self.user_info = {}
        self.collecting_info = False

    def handle_query(self, query, documents):
        response = self.process_query_with_llm(query, documents)
        return response

    def collect_user_info(self, message):
        if "name" not in self.user_info:
            self.user_info["name"] = message
            return "Got it! What's your phone number?"
        elif "phone" not in self.user_info:
            self.user_info["phone"] = message
            return "And your email?"
        elif "email" not in self.user_info:
            self.user_info["email"] = message
            return "Thank you! We will contact you soon."
        else:
            return "I have all the information I need. We will contact you soon."

    def handle_message(self, message, documents=None):
        if self.collecting_info:
            response = self.collect_user_info(message)
        elif "call me" in message.lower():
            self.collecting_info = True
            self.user_info = {}  # Reset user info
            response = "Sure, I can help with that. What's your name?"
        else:
            response = self.handle_query(message, documents)
        return response

    def process_query_with_llm(self, query, documents):
        prompt = f"Answer the following query based on the provided documents:\n\nQuery: {query}\n\nDocuments:\n"
        for doc in documents:
            prompt += f"- {doc}\n"
        
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()

# Sample documents
documents = [
    "Document 1 content about various topics...",
    "Document 2 content related to other topics...",
    "Document 3 content providing information on different subjects..."
]

# Create a Chatbot instance
chatbot = Chatbot()

# Example interactions
print(chatbot.handle_message("What is the capital of France?", documents))
print(chatbot.handle_message("Call me"))
print(chatbot.handle_message("John Doe"))
print(chatbot.handle_message("123-456-7890"))
print(chatbot.handle_message("john.doe@example.com"))
