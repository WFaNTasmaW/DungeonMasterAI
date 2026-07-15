from groq import Groq
from core.config import GROQ_API_KEY, LLM_MODEL


class LLMClient:

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = LLM_MODEL

    def chat(self, messages: list[dict]) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
        )

        return response.choices[0].message.content

    def ask(self, prompt: str) -> str:

        return self.chat(
            [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )

    def ask_json(self, prompt: str):

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.8,
            response_format={
                "type": "json_object"
            },
        )

        return response.choices[0].message.content