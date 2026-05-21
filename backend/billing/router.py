from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
async def billing_status():
    return {
        "plan": "free",
        "status": "active",
        "message": "Billing not yet configured"
    }

@router.post("/subscribe")
async def billing_subscribe():
    return {
        "message": "Billing coming soon"
    }
