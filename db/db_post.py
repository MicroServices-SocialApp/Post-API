from fastapi import HTTPException, status
from sqlalchemy import select, update as sql_update, delete as sql_delete
from schemas.schemas_post import PostModel, PostPatchModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from db.models import DbPost
# import asyncio

async def create(request: PostModel, db: AsyncSession):
    
    new_post = DbPost(
        text=request.text,
    )
    db.add(new_post)
    await db.commit()
    return new_post


# --------------------------------------------------------------------------


async def read_post_by_id(db: AsyncSession, id: int):

    query = select(DbPost).where(DbPost.id == id)
    result = await db.execute(query)
    post = result.scalar_one_or_none()
    return post


# --------------------------------------------------------------------------


async def read_all_posts(db: AsyncSession):

    query = select(DbPost)
    result = await db.execute(query)
    post = result.scalars().all()
    return post

# --------------------------------------------------------------------------

async def update(request: PostModel, db: AsyncSession, id: int):

    query = (
        sql_update(DbPost)
        .where(DbPost.id == id)
        .values(
            text=request.text,
        )
        .returning(DbPost)
    )

    result = await db.execute(query)
    await db.commit()
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return post

# --------------------------------------------------------------------------

async def patch(request: PostPatchModel, db: AsyncSession, id: int):
    # Convert request to a dictionary, keeping only the fields the user actually sent
    update_data = request.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The dict is empty')

    # Execute the update
    query = (
        sql_update(DbPost)
        .where(DbPost.id == id)
        .values(**update_data)  # Unpack the dict into the update query
        .returning(DbPost)
    )

    result = await db.execute(query)
    await db.commit()
    return result.scalar_one_or_none()

# --------------------------------------------------------------------------

async def delete(db: AsyncSession, id: int):
    query = sql_delete(DbPost).where(DbPost.id == id)
    await db.execute(query)
    await db.commit()
    return None
  
