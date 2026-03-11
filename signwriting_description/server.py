import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from signwriting.formats.fsw_to_sign import fsw_to_sign

from signwriting_description.gpt_description import describe_sign

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY environment variable")

app = FastAPI(title="Signwriting Description API")


@app.get("/health")
def health():
    return {"status": "ok"}


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
