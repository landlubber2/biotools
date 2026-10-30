import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, make_asgi_app

from datareader import get_fastx

fastxData = get_fastx()
app = fastapi.FastAPI()

REQSTS = Counter(
    "service_requests",
    "total HTTP requests",
    ["method", "status"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/metrics", make_asgi_app())


@app.middleware("http")
async def track_requests(request: fastapi.Request, call_next):
    if request.url.path.startswith("/metrics"):
        return await call_next(request)

    try:
        response = await call_next(request)
        status = str(response.status_code)
        return response
    except Exception:
        status = "500"
        raise
    finally:
        REQSTS.labels(
            method=request.method,
            status=status,
        ).inc()


@app.get("/")
def read_root():
    return {"status": "working"}


@app.get("/uniprot/{uniprot_id}")
def get_uniprot(uniprot_id: str):
    try:
        sequence = fastxData[uniprot_id]
        return {
            "uniprot_id": uniprot_id,
            "sequence": sequence,
        }
    except KeyError:
        raise fastapi.HTTPException(
            status_code=404,
            detail=f"Uniprot ID {uniprot_id} not found",
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
