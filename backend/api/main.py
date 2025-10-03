from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

from eva_core.orchestrator import EVAOrchestrator
from eva_core.policy_engine import PolicyEngine

app = FastAPI(title="EVA API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

eva_orchestrator = EVAOrchestrator()
policy_engine = PolicyEngine()


class MessageRequest(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"


class MessageResponse(BaseModel):
    content: str
    timestamp: str
    confidence: float


@app.on_event("startup")
async def startup_event():
    await eva_orchestrator.initialize()
    print("EVA API Server started")


@app.get("/")
async def root():
    return {
        "service": "EVA API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/status")
async def get_status():
    return eva_orchestrator.get_status()


@app.post("/chat", response_model=MessageResponse)
async def chat(request: MessageRequest):
    if not policy_engine.check_ethical_compliance(request.message):
        raise HTTPException(status_code=400, detail="Message violates ethical guidelines")
    
    response = await eva_orchestrator.process_message(
        request.message,
        request.user_id
    )
    
    return MessageResponse(**response)


@app.get("/ethics")
async def get_ethical_rules():
    return {"rules": policy_engine.get_rules()}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
