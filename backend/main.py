from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

from schemas import Emergency, Query, Draft
from database import create_document, get_documents, get_db

app = FastAPI(title="ResQ AI Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    status: str

@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "OK"}

@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")

@app.get("/test")
async def test_db() -> Dict[str, Any]:
    """Check database connectivity and basic CRUD."""
    try:
        db = await get_db()
        # Try listing collections
        collections = [c async for c in db.list_collection_names()]
        # Quick insert-read smoke test
        inserted = await create_document("ping", {"ping": "pong"})
        items = await get_documents("ping", {}, 1)
        return {
            "backend": "online",
            "database": "online",
            "database_url": "hidden",
            "database_name": db.name,
            "connection_status": "connected",
            "collections": collections,
            "sample": {"inserted": inserted, "fetched": items},
        }
    except Exception as e:
        return {
            "backend": "online",
            "database": "error",
            "connection_status": f"error: {type(e).__name__}: {e}",
        }

# Emergency Mode endpoint
@app.post("/emergency")
async def emergency(data: Emergency) -> Dict[str, Any]:
    saved = await create_document("emergency", data.model_dump())
    guidance = [
        "Ensure immediate safety and call local emergency services if needed.",
        "Document evidence: photos, messages, and witness details.",
        "We will reference applicable sections from BNS or UAE Penal Code based on your jurisdiction.",
    ]
    return {"saved": saved, "guidance": guidance}

# Law Mode endpoint
@app.post("/law")
async def law_query(data: Query) -> Dict[str, Any]:
    saved = await create_document("query", data.model_dump())
    answer = {
        "summary": "This is a concise answer based on available statutes and precedents.",
        "citations": [
            {"source": "BNS 2023 s.XX", "relevance": "high"},
            {"source": "UAE Penal Code Art.YY", "relevance": "medium"},
        ],
        "mode": data.depth,
    }
    return {"saved": saved, "answer": answer}

# Drafting endpoint
@app.post("/draft")
async def draft_doc(data: Draft) -> Dict[str, Any]:
    saved = await create_document("draft", data.model_dump())
    draft_text = f"Generated {data.doc_type} draft with jurisdiction {data.jurisdiction or 'N/A'}."
    improvements = [
        "Clarify indemnity and limitation of liability.",
        "Add governing law and jurisdiction clause.",
        "Include confidentiality obligations and term.",
    ]
    return {"saved": saved, "draft": draft_text, "suggestions": improvements}
