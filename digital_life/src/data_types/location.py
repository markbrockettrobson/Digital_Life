from pydantic import BaseModel


class Location(BaseModel):
    left: float
    right: float
    top: float
    bottom: float
