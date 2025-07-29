from pydantic import BaseModel

class DataModel(BaseModel):
    title : str
    url : str
    price : str