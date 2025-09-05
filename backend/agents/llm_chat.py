# backend/agents/llm_chat.py
from typing import List
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatResult
import requests
import os
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class FreeLLMWrapper(BaseChatModel):
    model_name: str = "mistralai/mistral-7b-instruct:free"
    base_url: str = "https://openrouter.ai/api/v1/chat/completions"
    api_key: str = os.getenv("OPENROUTER_API_KEY")

    def _generate(
        self,
        messages: List[HumanMessage],
        stop: List[str] = None,
        **kwargs
    ) -> ChatResult:
        if not self.api_key:
            raise ValueError("❌ OPENROUTER_API_KEY is not set in the environment!")
        
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        for attempt in range(3):
            try:
                payload = {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user" if isinstance(m, HumanMessage) else "assistant", "content": m.content}
                        for m in messages
                    ],
                }
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }

                response = session.post(self.base_url, json=payload, headers=headers, timeout=30)
                response.raise_for_status()

                result = response.json()
                if "choices" not in result or not result["choices"]:
                    raise RuntimeError("❌ OpenRouter returned no choices")

                content = result["choices"][0]["message"]["content"]
                ai_message = AIMessage(content=content)
                return ChatResult(generations=[ChatGeneration(message=ai_message)])
            
            except requests.exceptions.RequestException as e:
                print(f"❌ Attempt {attempt + 1}/3 failed: {e}")
                if attempt == 2:  # Last attempt
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff

    @property
    def _llm_type(self) -> str:
        return "custom-openrouter"