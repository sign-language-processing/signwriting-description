import os
from datetime import UTC, datetime

import httpx
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from signwriting.formats.fsw_to_sign import fsw_to_sign

from signwriting_description.gpt_description import describe_sign

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY environment variable")

TURNSTILE_SECRET_KEY = os.getenv("TURNSTILE_SECRET_KEY")

app = FastAPI(title="Signwriting Description API")

TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


@app.middleware("http")
async def turnstile_verification(request: Request, call_next):
    if request.url.path == "/health":
        return await call_next(request)

    token = request.headers.get("cf-turnstile-response")
    if not token:
        return JSONResponse(status_code=403, content={"error": "Missing Turnstile token"})

    async with httpx.AsyncClient() as client:
        result = await client.post(TURNSTILE_VERIFY_URL, data={
            "secret": TURNSTILE_SECRET_KEY,
            "response": token,
        })

    if not result.json().get("success"):
        return JSONResponse(status_code=403, content={"error": "Invalid Turnstile token"})

    return await call_next(request)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(tz=UTC).isoformat(),
        "service": "signwriting-description",
    }


@app.get("/")
def signwriting_description(
    fsw: str = Query(description="FSW string representing a sign"),
):
    if not fsw:
        raise HTTPException(status_code=400, detail="Missing `fsw` parameter")

    try:
        sign = fsw_to_sign(fsw)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid `fsw`: {e}") from e

    if not sign or len(sign.get("symbols", [])) == 0:
        raise HTTPException(status_code=400, detail="Empty `fsw` property")

    description = describe_sign(fsw)

    resp = JSONResponse(content={"description": description})
    resp.headers["Cache-Control"] = "public, max-age=2592000"  # 30 days
    return resp


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), reload=True)
