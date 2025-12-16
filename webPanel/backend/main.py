import os
import httpx
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
app = FastAPI()

load_dotenv(Path(__file__).resolve().parent / ".env")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLIENT_ID = os.environ["DISCORD_CLIENT_ID"]
CLIENT_SECRET = os.environ["DISCORD_CLIENT_SECRET"]
REDIRECT_URI = os.environ["DISCORD_REDIRECT_URI"]
FRONTEND_URL = os.environ["FRONTEND_URL"]


@app.get("/")
def home():
    return RedirectResponse("http://192.168.2.104:3000")

# ① ログイン開始
@app.get("/auth/discord/login")
def discord_login():
    scope = "identify guilds"
    url = (
        "https://discord.com/oauth2/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&scope={scope}"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return RedirectResponse(url)


# ② コールバック
@app.get("/auth/discord/callback")
async def discord_callback(code: str):
    token_url = "https://discord.com/api/oauth2/token"

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        token_res = await client.post(token_url, data=data, headers=headers)
        token_res.raise_for_status()
        token = token_res.json()

        access_token = token["access_token"]

        # ユーザー情報取得
        user_res = await client.get(
            "https://discord.com/api/users/@me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_res.raise_for_status()
        user = user_res.json()

    # 本番ではDB or セッションに保存
    print("Logged in user:", user["username"])

    # Reactへ戻す
    return RedirectResponse(f"{FRONTEND_URL}/dashboard")
