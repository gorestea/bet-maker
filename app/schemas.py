from pydantic import BaseModel, condecimal
from enum import Enum
from datetime import datetime
from typing import Optional

class BetStatus(str, Enum):
    not_played = "ещё не сыграла"
    won = "выиграла"
    lost = "проиграла"

class BetCreate(BaseModel):
    event_id: int
    amount: condecimal(gt=0, max_digits=10, decimal_places=2)

    class Config:
        json_schema_extra = {
            "example": {
                "event_id": 1,
                "amount": 100.00
            }
        }

class BetResponse(BaseModel):
    id: int
    event_id: int
    amount: condecimal(max_digits=10, decimal_places=2)
    status: BetStatus
    created_at: datetime
    result: Optional[str] = None  # Поле сделано опциональным

    class Config:
        use_enum_values = True
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "event_id": 1,
                "amount": 100.00,
                "status": "ещё не сыграла",
                "created_at": "2024-07-25T08:10:00",
                "result": "неизвестно"
            }
        }

class EventResponse(BaseModel):
    id: int
    name: str
    odds: condecimal(max_digits=5, decimal_places=2)
    deadline: datetime
    status: str

    class Config:
        use_enum_values = True
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Example Event",
                "odds": 1.25,
                "deadline": "2024-07-25 08:10",
                "status": "незавершённое"
            }
        }
