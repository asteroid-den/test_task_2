from fastapi import Request, HTTPException
from fastapi.routing import APIRouter

from services.database import DAO, models
from api_models import MultiChequeStatistics

router = APIRouter(prefix="/cheques", tags=["cheques"])

@router.get("/{cheque_id}")
async def get_cheque_statistics(request: Request, cheque_id: str) -> MultiChequeStatistics:
    author_id: int = request.state.uid  # type: ignore
    dao: DAO = request.state.dao  # type: ignore

    cheque = await dao.get_cheque_by_id(cheque_id=cheque_id)

    if not cheque:
        return HTTPException(status_code=404, detail="Cheque not found")

    if cheque.issuer_id != author_id:
        detail = "You do not have access since you're not cheque issuer"
        return HTTPException(status_code=403, detail=detail)
    
    activations: list[models.MultiChequeActivates] = await cheque.awaitable_attrs.activates

    response = MultiChequeStatistics(
        total_requests=cheque.activates_count,
        bots_blocked=None,
        multi_accounts_blocked=None,
        activations=len(activations),
        activations_by_country=dict()
    )

    return response