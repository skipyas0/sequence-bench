import openai
import os
from dotenv import load_dotenv

class ModelAPI():
    def __init__(self, model: str) -> None:
        self.model = model
        load_dotenv()
        self.client = openai.OpenAI(api_key=os.getenv("API_KEY"))
            
    def forward(self, messages, temp):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temp,
            n=1,
        )
        return completion
    
    def predict(self, question, temp, messages=[]) -> str:
        msgs = messages + [{"role": "user", "content": question}]

        try:
            completion = self.forward(
                messages=msgs,
                temp = temp
            )
        except openai.BadRequestError as e:
            print(f"WARNING: openai.BadRequestError for: {msgs}")
            completion = {"error": "openai.BadRequestError", "choices": [{"message": {"content": str(e)}}]}
        return completion.choices[0].message.content
    