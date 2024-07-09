import pydantic as pd


class Entity(pd.BaseModel):
    model_config = pd.ConfigDict(
        extra="forbid",
        validate_default=True,
        validate_assignment=True,
    )
