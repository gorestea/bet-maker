from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.schemas import BetCreate, BetResponse, EventResponse
from app.services.bet_service import BetService

router = APIRouter()

@router.get("/events", response_model=list[EventResponse])
async def get_events():
    """
    Получить список событий, доступных для ставок.
    """
    events = await BetService.get_available_events()
    return events

@router.post("/bet", response_model=BetResponse)
async def create_bet(bet: BetCreate = Body(...), db: AsyncSession = Depends(get_db)):
    """
    Совершить ставку на событие.

    - **event_id**: Идентификатор события
    - **amount**: Сумма ставки (должна быть положительным числом с двумя знаками после запятой)
    """
    return await BetService.create_bet(bet, db)

@router.get("/bets", response_model=list[BetResponse])
async def get_bets(db: AsyncSession = Depends(get_db)):
    """
    Получить историю ставок.
    """
    return await BetService.get_bets(db)
