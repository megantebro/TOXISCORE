import os, secrets, time
import httpx
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv
from shared.db import get_avg_rank,get_server_avg,get_today_stats,get_total_rank
load_dotenv()

CLIENT_ID = os.environ["DISCORD_CLIENT_ID"]
CLIENT_SECRET = os.environ["DISCORD_CLIENT_SECRET"]
REDIRECT_URI = os.environ["DISCORD_REDIRECT_URI"]
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")

# 超最小: メモリにセッション保存（本番はRedis/DB推奨）
SESSIONS: dict[str, dict] = {}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_session_token(req: Request) -> str | None:
    return req.cookies.get("session")

def require_session(req: Request) -> dict:
    tok = get_session_token(req)
    if not tok or tok not in SESSIONS:
        raise HTTPException(status_code=401, detail="Not logged in")
    return SESSIONS[tok]

@app.get("/auth/discord/login")
async def discord_login():
    # state は本番では保存して照合してね（最小なので省略寄り）
    state = secrets.token_urlsafe(16)
    scope = "identify guilds"
    url = (
        "https://discord.com/oauth2/authorize"
        f"?response_type=code&client_id={CLIENT_ID}"
        f"&scope={scope.replace(' ', '%20')}"
        f"&redirect_uri={httpx.URL(REDIRECT_URI)}"
        f"&state={state}"
    )
    return RedirectResponse(url)

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

    async with httpx.AsyncClient() as client:
        r = await client.post(token_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        r.raise_for_status()
        token_json = r.json()

        access_token = token_json["access_token"]

        me = await client.get(
            "https://discord.com/api/users/@me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        me.raise_for_status()

    session_token = secrets.token_urlsafe(24)
    SESSIONS[session_token] = {
        "access_token": access_token,
        "created_at": int(time.time()),
        "user": me.json(),
    }

    resp = RedirectResponse(f"{FRONTEND_URL}/dashboard")
    resp.set_cookie(
        "session",
        session_token,
        httponly=True,
        samesite="lax",
        # 本番HTTPSなら secure=True
    )
    return resp

@app.get("/api/me")
async def api_me(req: Request):
    s = require_session(req)
    return s["user"]

DISCORD_BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]

ADMINISTRATOR = 0x00000008

@app.get("/api/guilds")
async def api_guilds(req: Request):
    s = require_session(req)
    access_token = s["access_token"]

    async with httpx.AsyncClient() as client:
        # 1) ユーザーが所属してるサーバ（OAuth: guilds）
        r_user = await client.get(
            "https://discord.com/api/users/@me/guilds",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        r_user.raise_for_status()
        user_guilds = r_user.json()

        # 2) Botが所属してるサーバ（Bot token）
        r_bot = await client.get(
            "https://discord.com/api/users/@me/guilds",
            headers={"Authorization": f"Bot {DISCORD_BOT_TOKEN}"},
        )
        r_bot.raise_for_status()
        bot_guilds = r_bot.json()

    bot_ids = {g["id"] for g in bot_guilds}

    # 3) 管理者権限あり & Bot導入済み だけ残す
    filtered = []
    for g in user_guilds:
        perms = int(g.get("permissions", "0"))
        is_admin = (perms & ADMINISTRATOR) == ADMINISTRATOR
        has_bot = g["id"] in bot_ids
        if is_admin and has_bot:
            filtered.append(g)

    return filtered

@app.get("/api/guilds/{guild_id}/stats")
async def api_guild_stats(req: Request, guild_id: str):
    _ = require_session(req)

    today = get_today_stats(guild_id)
    avg_all = get_server_avg(guild_id)

    return {
        "guild_id": str(guild_id),
        "date": today["date"],
        "avg_today": today["avg_today"],
        "avg_all": avg_all,
    }

@app.get("/api/guilds/{guild_id}/rank/avg")
async def api_rank_avg(req: Request, guild_id: str, limit: int = 10, worst: bool = True):
    _ = require_session(req)
    return get_avg_rank(guild_id=guild_id, limit=limit, worst=worst)

@app.get("/api/guilds/{guild_id}/rank/total")
async def api_rank_total(req: Request, guild_id: str, limit: int = 10, worst: bool = True):
    _ = require_session(req)
    return get_total_rank(guild_id=guild_id, limit=limit, worst=worst)

@app.post("/api/logout")
async def api_logout(req: Request):
    tok = get_session_token(req)
    if tok:
        SESSIONS.pop(tok, None)
    resp = JSONResponse({"ok": True})
    resp.delete_cookie("session")
    return resp
