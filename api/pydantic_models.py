from pydantic import BaseModel
from typing import Optional,List

class QueryInput(BaseModel):
    query:str
    
class LLMResponse(BaseModel):
    output:str