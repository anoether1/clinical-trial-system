from fastapi import APIRouter, status

router = APIRouter()

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    include_in_schema=True,
    tags=["Status"],
    summary="Check server is running",
)
async def test_server():
    """
        Just testing the server is running or not
    """
    return {"msg": "Server is Running"}