from groq import Groq
import os 
import json

from dotenv import load_dotenv
load_dotenv()

client=Groq(api_key=os.getenv("GROQ_API_KEY"))
def explain(text:str,verdict:str,confidence:float)->dict:
    prompt=f"""You are a fact-checking expert. Analyze this news content and explain why it appears to be {verdict} with {confidence}% confidence.
Content: {text[:2000]}
Provide:
1. A 2-3 sentence explanation of why this content appears {verdict}
2. A list of 3-5 specific red flags or credibility indicators you noticed
3. A recommendation for the reader
Be specific about language patterns, claims made, and journalistic standards.
Respond in JSON format:
{{
    "explanation": "...",
    "red_flags": ["...", "...", "..."],
    "recommendation": "..."
}}"""
    
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        response_format={"type":"json_object"}

    )
    return json.loads(response.choices[0].message.content)

#json.loads() anedi converts json str to python dict 

