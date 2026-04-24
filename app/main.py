from fastapi import FastAPI
from app.api.routes import auth, reading
from fastapi.middleware.cors import CORSMiddleware

from mangum import Mangum

app = FastAPI()

app.include_router(auth.router)
app.include_router(reading.router)




app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],   # IMPORTANT: includes OPTIONS
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}

# ... your routes ...

# This is the Lambda handler entry point
handler = Mangum(app)