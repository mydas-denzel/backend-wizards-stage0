from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx
from datetime import datetime, timezone
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CAT_FACT_API = "https://catfact.ninja/fact"

@app.get("/me", response_class=JSONResponse)
async def get_profile():
    try:
        # Fetch cat fact dynamically
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(CAT_FACT_API)
            response.raise_for_status()
            data = response.json()
            cat_fact = data.get("fact", "No cat fact available.")
    except Exception:
        cat_fact = "Could not fetch cat fact at the moment."

    # Construct response JSON
    result = {
        "status": "success",
        "user": {
            "email": "okungbowadenzel65@gmail.com",
            "name": "Denzel Okungbowa",
            "stack": "Python/FastAPI"
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "fact": cat_fact
    }

    return JSONResponse(content=result, status_code=200)
