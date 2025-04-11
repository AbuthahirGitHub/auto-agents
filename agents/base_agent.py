from abc import ABC, abstractmethod
from typing import Any, Dict
import openai
from dotenv import load_dotenv
import os

load_dotenv()

class BaseAgent(ABC):
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.openai_api_key
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the input data and return the results
        """
        pass
    
    async def get_completion(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Get a completion from OpenAI's API
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant specialized in video creation."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error getting completion: {str(e)}")
            return "" 