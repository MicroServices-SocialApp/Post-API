from typing import Optional
from pydantic import BaseModel, Field


class PostModel(BaseModel):
    text: str = Field(
        default=Ellipsis,
        description="The text of the post.",
        deprecated=False,
        json_schema_extra={"example": "this video is cool."},
        # min_length=2,
        max_length=256,
    )
    
class PostPatchModel(BaseModel):
    text: Optional[str] = Field(
        default=None,
        description="The new text of the existing post.",
        deprecated=False,
        json_schema_extra={"example": "this video is NOT cool."},
        # min_length=2,
        max_length=256,
    )
#--------------------------------------------------------------------------

class PostDisplay(BaseModel):
    id: int
    text: str
    
    class ConfigDict:
        from_attributes = True
