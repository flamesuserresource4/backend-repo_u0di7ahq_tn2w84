import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import MenuItem, Reservation, Order

app = FastAPI(title="Restaurant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Restaurant API is running"}

# Helper to convert ObjectId
class Doc(BaseModel):
    id: str

# Menu endpoints
@app.get("/api/menu")
def list_menu(category: Optional[str] = None):
    filt = {"category": category} if category else {}
    items = get_documents("menuitem", filt)
    for it in items:
        it["id"] = str(it.pop("_id"))
    return items

@app.post("/api/menu", response_model=Doc)
def add_menu_item(item: MenuItem):
    inserted_id = create_document("menuitem", item)
    return {"id": inserted_id}

# Reservation endpoints
@app.post("/api/reservations", response_model=Doc)
def create_reservation(resv: Reservation):
    inserted_id = create_document("reservation", resv)
    return {"id": inserted_id}

@app.get("/api/reservations")
def list_reservations(limit: int = 50):
    docs = get_documents("reservation", {}, min(limit, 200))
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs

# Orders / Delivery
@app.post("/api/orders", response_model=Doc)
def place_order(order: Order):
    inserted_id = create_document("order", order)
    return {"id": inserted_id}

@app.get("/api/orders")
def list_orders(limit: int = 50):
    docs = get_documents("order", {}, min(limit, 200))
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
