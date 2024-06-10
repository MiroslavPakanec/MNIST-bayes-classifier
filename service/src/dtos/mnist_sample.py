from pydantic import BaseModel
from typing import List

class MNISTSample(BaseModel):
    data: List[int]