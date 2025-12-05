from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def judge_message(text: str) -> int:
    """暴言レベル 0〜5 を返す"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "暴言度を 0〜5 で数字のみ返してください。"},
            {"role": "user", "content": text}
        ]
    )

    score_text = response.choices[0].message.content.strip()

    try:
        return int(score_text)
    except:
        return 0
