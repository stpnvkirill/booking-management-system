from pydantic import BaseModel, Field, conint


class FeedbackCreate(BaseModel):
    booking_id: int = Field(..., example=1)
    rating: conint(ge=1, le=5) = Field(..., example=5)
    comment: str | None = Field(None, example="Всё понравилось!")


class FeedbackResponse(BaseModel):
    id: int
    booking_id: int
    rating: int
    comment: str | None

    class Config:
        from_attributes = True
