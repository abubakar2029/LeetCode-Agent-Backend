import os, time, jwt

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from requests import Session
from app import models
from app.utils.dbUtils import get_current_user, get_db
from app.services.github_service import (    
    exchange_code_for_token,
    get_user_email,
    get_user_info,
    get_user_repos,
)
from app.utils.security import decrypt_token, encrypt_token
from app.services.db_service import create_or_update_user

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/auth/callback"
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRES_SECONDS = 60 * 60 * 24 * 65  # 65 days
router = APIRouter(prefix="/auth", tags=["Auth"])

EXTENSION_REDIRECT=os.getenv("EXTENSION_REDIRECT")


@router.get("/login")
def auth_github(client_id: str, redirect_uri: str):
        return RedirectResponse(
        f"https://github.com/login/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=public_repo,user:email"
        f"&state={client_id}|{redirect_uri}"
    )


@router.get("/callback")
def auth_callback(code: str,state: str):

    ext_client_id, ext_redirect_uri = state.split("|")

    
    print("JWT_SECRET:", JWT_SECRET)
    print("JWT_ALGORITHM:", JWT_ALGORITHM)
    token_json = exchange_code_for_token(code)
    access_token = token_json.get("access_token")

    print("🔑 Token Response:", token_json)


    if not access_token:
        return HTMLResponse("<h1>Auth failed...</h1>", status_code=400)

    # user ka token sa os ki info get kr lan
    user_info = get_user_info(access_token)
    username = user_info.get("login")
    avatar_url = user_info.get("avatar_url")
    email = get_user_email(access_token)

    # 🔐 Encrypt before saving
    encrypted_token = encrypt_token(access_token)
    
    # Save in DB
    try:
        create_or_update_user( username, email, avatar_url, encrypted_token)
        payload = {
        "email": email,
        "username": username,
        "iat": int(time.time()),
        "exp": int(time.time()) + JWT_EXPIRES_SECONDS,
    }
        jwt_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        final_url = (
            f"{ext_redirect_uri}"
            f"?username={username}"
            f"&email={email}"
            f"&avatar_url={avatar_url}"
            f"&token={jwt_token}"
        )

        return RedirectResponse(final_url)


    except Exception as e:
        print("❌ DB save failed:", str(e))
        return HTMLResponse("<h1>Database error</h1>", status_code=500)



@router.get("/get-public-repo")
def list_repos(current_user: models.User = Depends(get_current_user)):
    try:
        token = decrypt_token(current_user.github_token)
        print("🔐 Decrypted token:", token)  
        repos = get_user_repos(token)
        return {"repos": repos}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@router.post("/confirm-repo")
def select_repo(repo_name: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.repo_name = repo_name
    db.commit()
    return {"message": "Repo selected", "repo_name": repo_name}



