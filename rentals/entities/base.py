import pydantic as pd


class Entity(pd.BaseModel):
    class Config:
        extra = pd.Extra.forbid
        validate_all = True
        validate_assignment = True
