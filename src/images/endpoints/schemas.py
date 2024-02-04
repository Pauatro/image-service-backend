from pydantic import BaseModel
from typing import List

class ImagePatientNameResponseBody(BaseModel):
    name: str

class ImagePixelArrayResponseBody(BaseModel):
    pixel_array: List[List[int]]