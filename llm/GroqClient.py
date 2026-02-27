import groq

class GroqClient:
    def __init__(self, api_key):
        self.client = groq.Client(api_key=api_key)

    def response(self, hist:list, model:str="llama-3.3-70b-versatile"):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. your answers are short and stright to the point"
                }
                ]+ hist,
            model=model
        )
        if not chat_completion or not chat_completion.choices or len(chat_completion.choices) == 0 or not chat_completion.choices[0].message :
            return "Client didn't work prop"
        return chat_completion.choices[0].message.content