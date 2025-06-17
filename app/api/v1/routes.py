# Combines all v1 routers

from fastapi import APIRouter
from app.schemas.user.user_schema import MatchRequest
from app.services.matcher import recommend_freelancers

# from app.api.v1.endpoints.user.user_endpoints import router as users_router

router = APIRouter()

# router.include_router(users_router, prefix="/users", tags=["Users"])


@router.get("/")
def root():
    return {"message": "Welcome to PeerHire API v1"}


#commited by Arham
@router.post("/recommend")
def recommend_top_freelancers(data: MatchRequest):
    return recommend_freelancers(data.project, data.freelancers)

routes=router