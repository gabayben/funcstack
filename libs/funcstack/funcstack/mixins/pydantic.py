from pydantic import BaseModel

class PydanticMixin(BaseModel):
    class Config:
        arbitrary_types_allowed = True