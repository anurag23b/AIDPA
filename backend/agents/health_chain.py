import os
import json
import httpx
import re
from dotenv import load_dotenv

load_dotenv()

async def run_health_chain(input_text: str):
    prompt = f"""
You are a health assistant. Analyze the user's symptoms and lifestyle.

Respond ONLY in this JSON format:
{{
  "status": "<brief summary of user’s health>",
  "recommendations": [
    "<advice 1>",
    "<advice 2>",
    "<advice 3>"
  ]
}}

Input:
{input_text}
"""

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "HTTP-Referer": "http://localhost",  # Required by OpenRouter
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",  # ✅ Free and available
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )
            if response.status_code != 200:
                print(f"❌ API returned non-200: {response.status_code}")
                print("❌ Response body:", response.text)
                return {"status": "Unparseable output", "recommendations": []}

            result = response.json()
            print("🔍 Full OpenRouter response:\n", result)

            content = result["choices"][0]["message"]["content"]
            print("🧠 Raw GPT output:\n", content)

            match = re.search(r"\{[\s\S]*?\}", content)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError as e:
                    print("⚠️ JSON parse error:", e)
                    print("⚠️ Raw text:\n", match.group())

        except Exception as e:
            print("❌ GPT error:", e)

    return {"status": "Unparseable output", "recommendations": []}
