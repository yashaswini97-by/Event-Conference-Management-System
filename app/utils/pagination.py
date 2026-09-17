from sqlalchemy.orm import Query


def paginate(
    query: Query,
    page: int = 1,
    limit: int = 10
):
    if page < 1:
        page = 1

    if limit < 1:
        limit = 10

    total = query.count()

    offset = (page - 1) * limit

    items = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_pages = (total + limit - 1) // limit

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages
    }