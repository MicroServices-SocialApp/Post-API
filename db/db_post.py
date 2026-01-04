from schemas.schemas_post import (
    PaginatedPostDisplay,
    PostDisplay,
    PostModel,
    PostPatchModel,
    ReadAllPost,
)
from sqlalchemy import select, update as sql_update, delete as sql_delete
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from db.models import DbPost


async def create(
    request: PostModel,
    db: AsyncSession,
    current_user_id: int,
) -> PostDisplay:
    new_post = DbPost(text=request.text, user_id=current_user_id)
    db.add(new_post)
    await db.commit()
    return PostDisplay.model_validate(new_post)


# --------------------------------------------------------------------------


async def read_post_by_id(
    post_id: int,
    db: AsyncSession,
) -> PostDisplay:
    query = select(DbPost).where(DbPost.id == post_id)
    result = await db.execute(query)
    post = result.scalar_one_or_none()
    return PostDisplay.model_validate(post)


# --------------------------------------------------------------------------


async def read_all_posts(
    limit: int,
    last_id: int | None,
    db: AsyncSession,
) -> PaginatedPostDisplay:
    
    query = select(DbPost).order_by(DbPost.id.desc()).limit(limit + 1)
    if last_id:
        query = query.where(DbPost.id < last_id)
    result = await db.execute(query)
    post = result.scalars().all()

    items = post[:limit]
    next_cursor: int | None = items[-1].id if items else None
    has_more: bool = len(post) > limit

    return PaginatedPostDisplay(
        items=[ReadAllPost.model_validate(p) for p in items],
        next_cursor=next_cursor if has_more else None,
        has_more=has_more,
    )


# --------------------------------------------------------------------------


async def update(
    post_id: int,
    request: PostModel,
    db: AsyncSession,
    current_user_id: int,
) -> PostDisplay:
    query = (
        sql_update(DbPost)
        .where(DbPost.id == post_id, DbPost.user_id == current_user_id)
        .values(
            text=request.text,
        )
        .returning(DbPost)
    )

    result = await db.execute(query)
    await db.commit()
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return PostDisplay.model_validate(post)


# --------------------------------------------------------------------------


async def patch(
    post_id: int,
    request: PostPatchModel,
    db: AsyncSession,
    current_user_id: int,
) -> PostDisplay:
    # Convert request to a dictionary, keeping only the fields the user actually sent
    update_data = request.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="The dict is empty"
        )

    # Execute the update
    query = (
        sql_update(DbPost)
        .where(DbPost.id == post_id, DbPost.user_id == current_user_id)
        .values(**update_data)  # Unpack the dict into the update query
        .returning(DbPost)
    )

    result = await db.execute(query)
    await db.commit()
    post = result.scalar_one_or_none()
    return PostDisplay.model_validate(post)


# --------------------------------------------------------------------------


async def delete(
    post_id: int,
    db: AsyncSession,
    current_user_id: int,
) -> None:
    query = sql_delete(DbPost).where(
        DbPost.id == post_id, DbPost.user_id == current_user_id
    )
    await db.execute(query)
    await db.commit()
    return None
