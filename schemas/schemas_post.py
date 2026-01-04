from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


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
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)


#------------------------------


class ReadAllPost(BaseModel):
    id: int
    text: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedPostDisplay(BaseModel):
    items: List[ReadAllPost]
    next_cursor: Optional[int]
    has_more: bool

    model_config = ConfigDict(from_attributes=True)