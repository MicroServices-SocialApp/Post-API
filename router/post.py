from typing import List
from fastapi import APIRouter, Depends, status
from auth.oauth2 import get_current_user
from db import db_post
from sqlalchemy.ext.asyncio.session import AsyncSession
from db.database import get_async_db
from schemas.schemas_post import PostModel, PostPatchModel, PostDisplay

router = APIRouter(prefix="/post", tags=["post"])


@router.post(
    "/create",
    include_in_schema=True,
    deprecated=False,
    name='Post_Creation',
    summary="Create a new Post",
    description="Registers a new post and saves its information into the PostgreSQL database.",
    response_model=PostDisplay,
    status_code=status.HTTP_201_CREATED,
    response_description="Post created successfully",
    responses={
        201: {
            "description": "SUCCESS - Post has been created",
            "content": {
                "application/json": {
                    "example": {"id": 1, "text": "this is a cool post."}
                }
            }
        },
        409: {
            "description": "CONFLICT"
        }
    }
)
async def create(request: PostModel, db: AsyncSession = Depends(get_async_db), current_user_id: int = Depends(get_current_user)):
    post = await db_post.create(request, db, current_user_id)
    return post


#--------------------------------------------------------------------------


@router.get(
    "/read_all_posts",
    include_in_schema=True,
    deprecated=False,
    name='Post_read_all',
    summary="Retrieve all posts",
    description="Returns a complete list of all posts stored in the PostgreSQL database.",
    response_model=List[PostDisplay],
    status_code=status.HTTP_200_OK,
    response_description="List of posts retrieved successfully",
    responses={
        200: {
            "description": "SUCCESS - Posts found",
            "content": {
                "application/json": {
                    "example": [{"id": 1, "text": "This is a cool text under a post."}]
                }
            }
        }
    }
)
async def read_all_posts(db: AsyncSession = Depends(get_async_db)):
    post = await db_post.read_all_posts(db)
    return post


#--------------------------------------------------------------------------


@router.put(
    "/update",
    include_in_schema=True,
    deprecated=False,
    name='Post_update',
    summary="Update an existing post",
    description="Perform a full update of a post's information. All fields in the request body are required.",
    response_model=PostDisplay,
    status_code=status.HTTP_200_OK,
    response_description="Post updated successfully",
    responses={
        200: {
            "description": "SUCCESS - Post information overwritten",
            "content": {
                "application/json": {
                    "example": {"id": 1, "text": "This is a NEW cool text under a post."}
                }
            }
        },
        404: {"description": "NOT FOUND - Post ID not found"}
    }
)
async def update(post_id: int, request: PostModel, db: AsyncSession = Depends(get_async_db), current_user_id: int = Depends(get_current_user)):
    post = await db_post.update(post_id, request, db, current_user_id)
    return post


#--------------------------------------------------------------------------


@router.patch(
    "/patch",
    include_in_schema=True,
    deprecated=False,
    name='Post_patch',
    summary="Partially update a post",
    description="Update specific fields of a post record without affecting the others.",
    response_model=PostDisplay,
    status_code=status.HTTP_200_OK,
    response_description="Post patched successfully",
    responses={
        200: {
            "description": "SUCCESS - Post fields updated",
            "content": {
                "application/json": {
                    "example": {"id": 1, "text": "This is a NEW NOT cool text under a post."}
                }
            }
        }
    }
)
async def patch(post_id: int, request: PostPatchModel, db: AsyncSession = Depends(get_async_db), current_user_id: int = Depends(get_current_user)):
    post = await db_post.patch(post_id, request, db, current_user_id)
    return post

#--------------------------------------------------------------------------

@router.delete(
    "/delete",
    include_in_schema=True,
    deprecated=False,
    name='Post_delete',
    summary="Delete a post from the database",
    description="Permanently removes a user record from the PostgreSQL database using their unique ID.",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Post deleted successfully",
    responses={
        204: {
            "description": "SUCCESS - Post has been deleted",
        },
        500: {
            "description": "SERVER ERROR - Database failure during deletion",
            "content": {
                "application/json": {
                    "example": {"detail": "Error - Post could not be deleted from the database."}
                }
            }
        }
    }
)
async def delete(post_id: int, db: AsyncSession = Depends(get_async_db), current_user_id: int = Depends(get_current_user)):
    await db_post.delete(post_id, db, current_user_id)
    return None