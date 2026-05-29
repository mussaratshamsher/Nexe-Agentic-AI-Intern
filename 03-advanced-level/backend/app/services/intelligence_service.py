from groq import AsyncGroq
from ..config.settings import settings
import json

client = AsyncGroq(api_key=settings.GROQ_API_KEY)
# Use 8B for simple classification tasks to save tokens and latency
SMALL_MODEL = "llama-3.1-8b-instant"

class IntelligenceService:
    @staticmethod
    async def analyze_sentiment(text: str):
        prompt = f"""
        Analyze the sentiment of the following text. 
        Return a JSON object with 'sentiment' (one of: Positive, Neutral, Negative, Frustrated, Excited) 
        and 'score' (an integer from 0 to 100 where 100 is most positive/excited).

        Text: {text}
        """
        try:
            response = await client.chat.completions.create(
                model=SMALL_MODEL,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Sentiment Analysis Error: {e}")
            return {"sentiment": "Neutral", "score": 50}

    @staticmethod
    async def calculate_lead_score(customer_data: dict, interactions: list):
        prompt = f"""
        Evaluate this lead based on their profile and interaction history.
        Return a JSON object with 'score' (0-100) and 'status' (one of: cold, warm, hot, converted).

        Profile: {customer_data}
        Recent Interactions: {interactions}
        """
        try:
            response = await client.chat.completions.create(
                model=SMALL_MODEL,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Lead Scoring Error: {e}")
            return {"score": 10, "status": "cold"}
