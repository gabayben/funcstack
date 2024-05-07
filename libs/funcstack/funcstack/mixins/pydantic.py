from pydantic import BaseModel

class PydanticMixin(BaseModel):
    class Config:
        extra = 'allow'
        arbitrary_types_allowed = True