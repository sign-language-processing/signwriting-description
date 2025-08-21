from __future__ import annotations

import hashlib
import os
from pathlib import Path

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

DISKCACHE_DIR = os.getenv("DISK_CACHE_DIR")
cache: Cache | None = None
if DISKCACHE_DIR:
    from diskcache import Cache

    path = Path(DISKCACHE_DIR).expanduser()
    print("Using disk cache at", path)
    path.mkdir(parents=True, exist_ok=True)
    cache = Cache(str(path))

app = FastAPI(title="Signwriting Description API")


@app.get("/")
def signwriting_description(
    fsw: str = Query(description="FSW string representing a sign"),
):
    if not fsw:
        raise HTTPException(status_code=400, detail="Missing `fsw` parameter")

    # Validate FSW parses and isn't empty
    try:
        sign = fsw_to_sign(fsw)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid `fsw`: {e}") from e

    if not sign or len(sign.get("symbols", [])) == 0:
        raise HTTPException(status_code=400, detail="Empty `fsw` property")

    fsw_hash = hashlib.md5(fsw.encode("utf-8")).hexdigest()
    key = f"descriptions:{fsw_hash}"
    print("Cache key:", key)

    description = None
    cache_hit = False

    if cache is not None:
        cached: str | None = cache.get(key)
        if cached is not None:
            print("Cache hit")
            description, cache_hit = cached, True

    if description is None:
        print("Input:", fsw)
        description = describe_sign(fsw)
        print("Output:", description)

        if cache is not None:
            cache.set(key, description)

    resp = JSONResponse(content={
        "description": description,
        "cache_hit": cache_hit
    })
    resp.headers["Cache-Control"] = "public, max-age=2592000"  # 30 days
    return resp


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), reload=True)
