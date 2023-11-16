from pydantic import BaseModel


class OrmBaseModel(BaseModel):
    class ConfigDict:
        orm_mode = True
