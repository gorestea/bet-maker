from datetime import datetime
import httpx
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Bet
from app.schemas import BetCreate, BetResponse, EventResponse, BetStatus

class BetService:

    @staticmethod
    async def get_available_events() -> list[EventResponse]:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://line-provider:8000/events")
            response.raise_for_status()
            events_data = response.json()

            now = datetime.utcnow()

            available_events = [
                EventResponse(**event) for event in events_data
                if datetime.fromisoformat(event['deadline']) > now and event['status'] == 'незавершённое'
            ]
            return available_events

    @staticmethod
    async def create_bet(bet_data: BetCreate, db: AsyncSession) -> BetResponse:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://line-provider:8000/events/{bet_data.event_id}")
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Событие не найдено")
            event_data = response.json()
            if event_data["status"] != "незавершённое":
                raise HTTPException(status_code=400, detail="Нельзя поставить ставку на завершённое событие")

        new_bet = Bet(
            event_id=bet_data.event_id,
            amount=bet_data.amount,
            status=BetStatus.not_played,  # статус "ещё не сыграла"
            created_at=datetime.utcnow()
        )
        db.add(new_bet)
        await db.commit()
        await db.refresh(new_bet)
        return BetResponse.from_orm(new_bet)

    @staticmethod
    async def get_bets(db: AsyncSession) -> list[BetResponse]:
        async with db.begin():
            result = await db.execute(select(Bet))
            bets = result.scalars().all()

            bet_responses = []
            async with httpx.AsyncClient() as client:
                for bet in bets:
                    response = await client.get(f"http://line-provider:8000/events/{bet.event_id}")
                    event_data = response.json()

                    # Определение статуса ставки на основе статуса события
                    if event_data["status"] == "незавершённое":
                        result_text = "ещё не сыграла"
                        bet.status = BetStatus.not_played
                    elif event_data["status"] == "завершено выигрышем первой команды":
                        result_text = f"выигрыш: {round(float(bet.amount) * float(event_data['odds'])), 2}"
                        bet.status = BetStatus.won
                    else:
                        result_text = "проиграла"
                        bet.status = BetStatus.lost

                    # Обновление статуса в базе данных

                    bet_responses.append(BetResponse.from_orm(bet).copy(update={"result": result_text}))

            await db.commit()

        return bet_responses
