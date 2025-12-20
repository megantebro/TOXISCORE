from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import json
from MessageData import MessageData

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def judge_message(messages: list):
    
    for message in messages:
        if len(message.content) >= 30:
            messages.remove(message.content)


    """
    messages: List[MessageData]
    return: List[int] (各メッセージのスコア)
    """

    # MessageData → テキスト化
    text_list = "\n".join(
        [f"{i+1}. {m.user.display_name}: {m.content}" for i, m in enumerate(messages)]
    )

    prompt = f"""
    以下のメッセージそれぞれに 0〜100 の暴言スコアをつけてください。
    出力は JSON の配列のみ。説明文は禁止。

    メッセージ:
    {text_list}

    例: [12, 0, 55, 3, 90, 0, 8, 1, 0, 13]
    """

    # 新 API（v1.x）形式

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    except:
        return [0] * len(messages) 
    

    raw = response.choices[0].message.content.strip()

    try:
        scores = json.loads(raw)
        if isinstance(scores, list):
            print(text_list)
            print(scores)
            return scores
    except:
        pass

    # パース失敗時は全部0
    return [0] * len(messages)
